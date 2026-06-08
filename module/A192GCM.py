from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def enc(key, payload, iv, aad):
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(iv, payload, associated_data=aad)
    return ciphertext

def main(key, payload, iv, aad):
    try:
        return enc(key, payload, iv, aad)
    except Exception as e:
        key = os.urandom(24)
        return enc(key, payload, iv, aad)
