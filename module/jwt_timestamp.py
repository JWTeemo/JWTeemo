import time
import random

def main():
    return str(int(time.time()) + random.randint(-10, 10)).encode()

if __name__ == "__main__":
    print(main())