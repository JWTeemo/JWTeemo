def main(data: bytes, enc: bytes):
    tag_lengths = {
        b"A128CBC-HS256": 16,
        b"A192CBC-HS384": 24,
        b"A256CBC-HS512": 32,
        b"A128GCM": 16,
        b"A192GCM": 16,
        b"A256GCM": 16,
        b"A128GCMKW": 16,
        b"A192GCMKW": 16,
        b"A256GCMKW": 16,
    }
    tag_len = tag_lengths.get(enc)
    if tag_len is None:
        raise ValueError(f"Unsupported enc: {enc}")
    return data[:-tag_len]
