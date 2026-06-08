from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hmac, hashes, padding
import os

def sign(key, payload, iv, aad):
    if len(key) != 32:
        raise ValueError("Key length must be 32 bytes for A128CBC-HS256")

    mac_key = key[:16]
    enc_key = key[16:]

    padder = padding.PKCS7(128).padder()
    padded = padder.update(payload) + padder.finalize()

    cipher = Cipher(algorithms.AES(enc_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    al = (8 * len(aad)).to_bytes(8, byteorder='big')
    h = hmac.HMAC(mac_key, hashes.SHA256())
    h.update(aad + iv + ciphertext + al)
    tag = h.finalize()[:16]

    return ciphertext + tag

def main(key, payload, iv, aad):
    try:
        return sign(key, payload, iv, aad)
    except Exception as e:
        key = os.urandom(32)
        return sign(key, payload, iv, aad)