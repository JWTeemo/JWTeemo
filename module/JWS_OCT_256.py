from base64 import urlsafe_b64decode

def decode_base64url(data):
    data += '=' * (-len(data) % 4)
    return urlsafe_b64decode(data)

def main():
    key_b64 = "9N3QK6Y1BjCQijFaVqwwp_-Jq3zhUqIxdeUr-Mfy4Rs"
    key = decode_base64url(key_b64)
    return key