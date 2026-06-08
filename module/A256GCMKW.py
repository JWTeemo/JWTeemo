from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
from base64 import urlsafe_b64decode

def sign(key, payload, iv):
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(iv, payload, associated_data=None)
    return ciphertext

def main(key, payload, iv):
    try:
        return sign(key, payload, iv)
    except Exception as e:
        key = os.urandom(32)
        return sign(key, payload, iv)