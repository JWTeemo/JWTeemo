from base64 import urlsafe_b64decode

def decode_base64url(data):
    data += '=' * (-len(data) % 4)
    return urlsafe_b64decode(data)

def main():
    key_b64 = "v-LkpNJpJvrdB9539Zg76PH3etQXGHymvFj6Ttg-dOVhj8iSsxTUpXPRwrkoEScBHm8R5XnYNYkMXuZAA6QY3Q"
    key = decode_base64url(key_b64)
    return key