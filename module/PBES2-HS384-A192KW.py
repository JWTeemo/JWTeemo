from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, keywrap
from cryptography.hazmat.backends import default_backend

def main(key, cek: bytes, p2s: bytes, p2c = 1000):
    password = key
    salt = b"PBES2-HS384+A192KW" + b"\x00" + p2s

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA384(),
        length=24,  # 192-bit KEK
        salt=salt,
        iterations=p2c,
        backend=default_backend()
    )
    kek = kdf.derive(password)

    ek = keywrap.aes_key_wrap(kek, cek, backend=default_backend())
    return ek