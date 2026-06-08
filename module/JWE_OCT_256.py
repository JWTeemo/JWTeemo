from base64 import urlsafe_b64decode

def decode_base64url(data):
    data += '=' * (-len(data) % 4)
    return urlsafe_b64decode(data)

def main():
    key_b64 = "721ypyw1BIFVk0xcmhPfKg6ypH9wAmmtGrVNZpSXV3k"
    key = decode_base64url(key_b64)
    return key