# Initially, it was compatibily code in case that pyOpenSSL is not installed,
# which explains why the API matches OpenSSL.crypto.
# But the latter was dropped in favor of cryptography, which is still not
# pure-Python and slapos.buildout still can't bootstrap with it so most of
# the time we fall back on this module.
# Rewriting to match the cryptography API is not worth it.

import os
from contextlib import contextmanager
from fcntl import fcntl, F_SETFD, F_GETFD, FD_CLOEXEC
from subprocess import Popen, PIPE, STDOUT
from threading import Thread

class Error(Exception): pass

FILETYPE_PEM = 1

class X509(object):
  pass

@contextmanager
def _pipe(data):
  def write():
    os.write(w, data)
    os.close(w)
  r, w = os.pipe()
  try:
    # Py3: stop using fcntl+close_fds=False and use pass_fds
    fcntl(r, F_SETFD, fcntl(r, F_GETFD) & ~FD_CLOEXEC) # no-op on Py2
    fcntl(w, F_SETFD, fcntl(w, F_GETFD) | FD_CLOEXEC)  # no-op on Py3
    t = Thread(target=write)
    t.daemon = True
    t.start()
    yield '/proc/self/fd/%u' % r
  finally:
    os.close(r)

def dump_publickey(type, pkey):
  assert type == FILETYPE_PEM, type
  if pkey.startswith(b'-----BEGIN PUBLIC KEY-----'):
    return pkey
  with _pipe(pkey) as pkey:
    p = Popen(("openssl", "rsa", "-in", pkey, "-pubout"),
              stdout=PIPE, stderr=PIPE, close_fds=False)
  r, err = p.communicate()
  if p.poll():
    raise Error(err)
  return r

def load_privatekey(type, buffer):
  assert type == FILETYPE_PEM, type
  return buffer.encode()

def load_certificate(type, buffer):
  # extract public key since we only use it to verify signatures
  assert type == FILETYPE_PEM, type
  p = Popen(("openssl", "x509", "-pubkey", "-noout"),
            stdin=PIPE, stdout=PIPE, stderr=PIPE)
  out, err = p.communicate(buffer.encode())
  if p.poll():
    raise Error(err)
  cert = X509()
  cert.get_pubkey = lambda: out
  return cert

def sign(pkey, data, digest):
  with _pipe(pkey) as pkey:
    p = Popen(("openssl", digest, "-sign", pkey),
              stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=False)
  out, err = p.communicate(data)
  if p.poll():
    raise Error(err)
  return out

def verify(cert, signature, data, digest):
  with _pipe(cert.get_pubkey()) as key, _pipe(signature) as sign:
    p = Popen(("openssl", digest, "-verify", key, "-signature", sign),
              stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=False)
    err = p.communicate(data)[0]
  if p.poll():
    raise Error(err)
