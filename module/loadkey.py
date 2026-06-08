from base64 import urlsafe_b64decode

JWE_OCT_128 = {"k": "-f0Y7I6r0W8bQOmbtpU7Ew", "kty": "oct"}
JWE_OCT_192 = {"k": "W37LwFVQTCZRVLsf4yVqK1RzQOQ8EhjG", "kty": "oct"}
JWE_OCT_256 = {"k": "721ypyw1BIFVk0xcmhPfKg6ypH9wAmmtGrVNZpSXV3k", "kty": "oct"}
JWE_OCT_384 = {"k": "RcCAvOYF5MO8mt9GfcLTPEJvCYW1KKLcFKgVwQZ2aHO5lj-hz5CGkomNY5UOlW-R", "kty": "oct"}
JWE_OCT_512 = {"k": "v-LkpNJpJvrdB9539Zg76PH3etQXGHymvFj6Ttg-dOVhj8iSsxTUpXPRwrkoEScBHm8R5XnYNYkMXuZAA6QY3Q", "kty": "oct"}

def b64url_decode(data):
    padded = data + '=' * (-len(data) % 4)
    return urlsafe_b64decode(padded)

def main(enc_value):
    if enc_value == b"A128GCM":
        return b64url_decode(JWE_OCT_128["k"])
    elif enc_value == b"A192GCM":
        return b64url_decode(JWE_OCT_192["k"])
    elif enc_value == b"A256GCM":
        return b64url_decode(JWE_OCT_256["k"])
    elif enc_value == b"A128CBC-HS256":
        return b64url_decode(JWE_OCT_256["k"])  # 32 bytes = 16 + 16
    elif enc_value == b"A192CBC-HS384":
        return b64url_decode(JWE_OCT_384["k"])  # 48 bytes = 24 + 24
    elif enc_value == b"A256CBC-HS512":
        return b64url_decode(JWE_OCT_512["k"])  # 64 bytes = 32 + 32
    else:
        raise ValueError(f"Unsupported enc algorithm: {enc_value}")

if __name__ == "__main__":
    for enc in ["A128GCM", "A256CBC-HS512"]:
        key_bytes = main(enc)
        print(f"{enc} key ({len(key_bytes)} bytes):", key_bytes.hex())
