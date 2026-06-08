from base64 import urlsafe_b64decode

def decode_base64url(data):
    data += '=' * (-len(data) % 4)
    return urlsafe_b64decode(data)

def main():
    key_b64 = "ZCQFA1ENCSknpLSlD0SJOAr7cru09l9eUdutIX1TuT1A9_vMhmnMRI9sllNvssQW"
    key = decode_base64url(key_b64)
    return key