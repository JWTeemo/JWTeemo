import hmac
import hashlib
import os
from base64 import urlsafe_b64decode, urlsafe_b64encode

def decode_base64url(data):
    data += '=' * (-len(data) % 4)
    return urlsafe_b64decode(data)

def sign(key, payload):
    sig = hmac.new(key, payload, hashlib.sha384).digest()
    return sig

def main(key, payload):
    try:
        return sign(key, payload)
    except Exception as e:
        key = os.urandom(48)
        return sign(key, payload)

if __name__ == "__main__":
    print(main(b"123", b"Hello World!"))
