from cryptography.hazmat.primitives.keywrap import aes_key_wrap, aes_key_unwrap
import os

def sign(key, payload):
    wrapped_key = aes_key_wrap(key, payload)
    return wrapped_key

def main(key, payload):
    try:
        return sign(key, payload)
    except Exception as e:
        key = os.urandom(32)
        return sign(key, payload)