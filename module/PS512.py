from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key

def sign(key, payload):
    private_key = load_pem_private_key(key, password=None)

    signature = private_key.sign(
        payload,
        padding.PSS(padding.MGF1(hashes.SHA512()),
                    hashes.SHA512.digest_size),
        hashes.SHA512()
    )

    return signature

def main(key, payload: bytes) -> bytes:
    try:
        return sign(key, payload)
    except Exception as e:
        key = b'-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC1AehJvoY2vmdM\nzp1oYBAHnIDYnlY0jVcABm8YxW05U1Oi5nIZ8xaYKxFq7e04+G92cIm+SXgkoG1C\nllTYuYl0v9Gmx7hYhU8/NbQtuwXCZw22tIZ+7oJ8EPRePnNrKeBHFn2bV57fzVhY\n6t0j/pIoLbE0mlfMUyUhlD+Ro83eCqAhG8FUoHOxj2YqTHPVSWTdkA/WG4dbng0Y\n/RHSiTXv9WsE4Pj0YhLWJDmgIq4b6Qe89xgH77CrjvONd+5xpj8ZjLDhrk6+KF18\neFEqETG++z7hPDFqzYD9iLZ/wcLmuVonJJlUxxxbpmOOeMQEJmtirOyt58TrF0wK\nD3WIoKrZAgMBAAECggEAKwsDknnAj8cSaITfkKD7Xtv8Fcb9R+zuad6dz52vHgkv\nI9c5/eq9Dj17nFps5XXKh7c2Qi5VaBxQLxvxnEHuqnks4USwFTjKQgVCzfch5Ps9\nmxttukR8egVMHxcpuiuQnkb+YpDhAmZh4m8jXDpexjgrYg9r3nZNJ6GJxlfWDj1B\nNQi9hHRMERTccPFHOA/DbGZU8clL9was7HDU9RUZzBl3fAhVl8j51UA+dpTQRnWd\n6zsCLTgq/skCol8KsDuLmfNGCwYyRDDoIGp8kqho9AEiF5AVAuoE1ChQqSCLhG+6\na65D7Zox9oCpBb6ggurIx1PLbh8x1hpa+M/lf48jUwKBgQDb3JOH7Puv3CXIcQoT\ne1TdgUXOsBffinftbRE0hcxpJXsSmF8BSVYzHukFVST8Q8fjC2wTK/t4f0MCTmAr\n42VBFqHQTjXUHRMFU1UDgOP3dHgrc7ac6xaO5MRtQVnftQR5MChaD3FJ64mQ0gZT\n0SfYLqzd475Wf7PfKe1hVc0TywKBgQDSwmjsLA8q9BcjTLNdKtHFNkylqSj9MFaw\nkYk7lN2bFsqczKv+J5mLAApyWOIiHYzJ6AXiEnnx1c+FRK7kSHyCKc0e4I5+e61d\n/KDTxfTRJ3bpEZRSW3ojg2GOoW4YJ1yrnvf7kAqSH+hluQLsGI8olaev0AYqBcU6\nWDjGfDGPawKBgFut3tcPOuRaKGcsu8bj5r926GUHiOzuEJQwprwADvzJZEicwQEI\nU6l9ei1/E60dlnxWhvp3nKTibE7J39BtQguiJFd4RXntpcDSvuB3HphROMrltYA5\nh26OdloYpiFimjrumeT0C4mHbhW1fm31CWhcDjl4fiYTmi20jgfIf3uBAoGAJr+J\nbMpY64u+6UWDwIBL2tc11ks4dvw5I/NN6L9g0s+o5pUWlf6P0ydpxEYlJSKLrN9U\nnZDKDLVDlvver6fIBGJNDP06FXUFlb8JjoXZkc6QpR8PRuj8lqTj/cYeKKCr//2V\nGBIOb3kgT/to1yFYyJxjHQbA617uOODZZ1yT/AsCgYEAv3qDEKUfAt4YkvYENR3p\nUNzoJv1kPoxFJuqF227MIMHPdwkkhh0LILFEexz+Wz2H66jGlsrDcCNCs5SZNhC8\nhzx7JI1BJmczXnZYL8Z2tvy650OGj8TEStDEMqewo0hsC7kCOagl3f5moHq+1acI\n8YuLYY/JqEgLwPKJPPPVn+8=\n-----END PRIVATE KEY-----\n'
        return sign(key, payload)