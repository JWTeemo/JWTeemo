from base64 import urlsafe_b64decode

def decode_base64url(data):
    data += '=' * (-len(data) % 4)
    return urlsafe_b64decode(data)

def main():
    key_b64 = "a1J80O7AtzdxrJWPvZ-dkxBNV_UHKPAONlusaOT-mMHRi8hw5UARVMouGr-AFsvKLGJ8u_T_hFAIS3oZCUHEpQ"
    key = decode_base64url(key_b64)
    return key