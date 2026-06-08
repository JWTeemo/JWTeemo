import base64

def main(data: bytes):
    # print(data)
    return base64.urlsafe_b64encode(data).rstrip(b'=')

if __name__ == '__main__':
    text = b"Hello, World!"
    print(main(text))