def main(header):
    if b"zip" in header:
        return b"True"
    else:
        return b"False"