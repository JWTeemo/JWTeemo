import os
def main(enc):
    iv_size = 12  # default for GCM
    if b"CBC" in enc:
        iv_size = 16
    return os.urandom(iv_size)