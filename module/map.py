def main(a, b):
    try:
        if b.decode().isdigit() or b.startswith(b"{"):
            # print(b)
            return b"\"" + a + b"\"" + b":" + b
        else:
            return b"\"" + a + b"\"" + b":" + b"\"" + b + b"\""
            # return f'"{a.decode()}":"{b.decode()}"'.encode()
    except Exception as e:
        return b"\"" + a + b"\"" + b":" + b"\"" + b + b"\""

if __name__ == '__main__':
    print(main(b"a", b"1"))
    print(main(b"a", b"a"))