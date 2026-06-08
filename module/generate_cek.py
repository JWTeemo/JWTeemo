import os
def main(enc):
    size = 64
    if b"A128GCM" in enc:
        size = 16
    elif b"A192GCM" in enc:
        size = 24
    elif b"A256GCM" in enc:
        size = 32
    elif b"A128CBC-HS256" in enc:
        size = 32
    elif b"A192CBC-HS384" in enc:
        size = 48
    elif b"A256CBC-HS512" in enc:
        size = 64
    return os.urandom(size)