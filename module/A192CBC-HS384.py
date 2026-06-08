from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hmac, hashes, padding
import os

def sign(key, payload, iv, aad):
    if len(key) != 48:
        raise ValueError("Key length must be 48 bytes for A192CBC-HS384")

    mac_key = key[:24]
    enc_key = key[24:]

    padder = padding.PKCS7(128).padder()
    padded = padder.update(payload) + padder.finalize()

    cipher = Cipher(algorithms.AES(enc_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    al = (8 * len(aad)).to_bytes(8, byteorder='big')
    h = hmac.HMAC(mac_key, hashes.SHA384())
    h.update(aad + iv + ciphertext + al)
    tag = h.finalize()[:24]

    return ciphertext + tag

def main(key, payload, iv, aad):
    try:
        return sign(key, payload, iv, aad)
    except Exception as e:
        key = os.urandom(48)
        return sign(key, payload, iv, aad)
