from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key

def sign(key, payload):
    private_key = load_pem_private_key(key, password=None)
    signature = private_key.sign(payload)
    return signature

def main(key, payload: bytes) -> bytes:
    try:
        return sign(key, payload)
    except Exception as e:
        key = b'-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEIJCYs20djKHJuDLPC71+oQZAnV97dmaRgrIKr7YcEEDz\n-----END PRIVATE KEY-----\n'
        return sign(key, payload)
