from base64 import urlsafe_b64decode

def decode_base64url(data):
    data += '=' * (-len(data) % 4)
    return urlsafe_b64decode(data)

def main():
    key_b64 = "RcCAvOYF5MO8mt9GfcLTPEJvCYW1KKLcFKgVwQZ2aHO5lj-hz5CGkomNY5UOlW-R"
    key = decode_base64url(key_b64)
    return key