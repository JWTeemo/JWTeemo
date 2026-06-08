def main(s):
    try:
        return b"{" + s + b"}"
    except Exception as e:
        print(s)
        print(f"Error: {e}")

if __name__ == '__main__':
    print(main(b'"a":"b"'))