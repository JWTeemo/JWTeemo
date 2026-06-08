import hmac
import hashlib
import os
from base64 import urlsafe_b64decode, urlsafe_b64encode

def decode_base64url(data):
    data += '=' * (-len(data) % 4)
    return urlsafe_b64decode(data)

def sign(key, payload):
    sig = hmac.new(key, payload, hashlib.sha256).digest()
    return sig

def main(key, payload):
    try:
        return sign(key, payload)
    except Exception as e:
        key = os.urandom(32)
        return sign(key, payload)

if __name__ == "__main__":
    payload = b"eyJhbGciOiJIUzI1NiIsImFsZyI6IlJTMjU2In0.eyIxIjoiMiJ9."
    key = b"""-----BEGIN PUBLIC KEY-----
    MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAr9SS/Xo8ICHdcFstHmVk
    JnEKWvRLx5EEdgjayb4HULSbfNaNZ0V9qoMkD/+/thdFfH/zC1rLW0eion8rkbNU
    yT9i0MJM5IK8vjGe3zATkv8y8MYPfNeAC75TbBaP9qZQET3d+Ql4j73SyIhfNHH1
    Tz/6ivxW292QQ7O4ZJAEAnQFJhMUKxwAQTda4v0tmZXgYoXDwpl4qJeubke1e2DA
    8Mr62qeW8+pD0zS1GJDEq5tqURi5Zat2S+ReaYnWpZ7kOAbQsvO4AxynLB1hAVEL
    XMLMWbijKuDvsIh4hT3sss7OsiqUWaRskHcGfvS2ou16KgKNgyZligNYf35r8s07
    6QnEDFMnGpVt6l4B/jo4DjVCCSlABZ9Lkk5vhi3Hi+GZV8ERmc+Rav0WtM6wmtCg
    7OxebnETQx4Zz00Mbf5NIesg7mYANxBqC7UqCXRBHEXlM4bItOGOnBKVcXUX/e5u
    9UMVHd1A5IhGQUk6qadQ0jOTDA63vg6YSEY8RTaYpDGBM40rObSE5iUQu6XV0TY+
    v4ERmY/SDKBWEuLZ+BOI9oULJanzIredHjMy3anMxnl0AKhLMaSSMpxgpqSHuHNc
    q4Ta7QndbgZgZHFZMXpF8F6d1sZVY5GoLY+8yTkgV5fzuAHGxYz+6rOdXt90nLXt
    kC32lrlXGZ3gtVSOvadCLaMCAwEAAQ==
    -----END PUBLIC KEY-----"""
    print(payload + urlsafe_b64encode(main(key, payload)))
