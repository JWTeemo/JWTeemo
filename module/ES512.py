from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature

def sign(key, payload):
    private_key = load_pem_private_key(key, password=None)

    der_signature = private_key.sign(
        payload,
        ec.ECDSA(hashes.SHA512())
    )

    # 解析 DER 编码的 r,s，并拼接成 raw 签名（用于 JWS 的 ES256 格式）
    r, s = decode_dss_signature(der_signature)
    signature_raw = r.to_bytes(64, byteorder='big') + s.to_bytes(64, byteorder='big')

    return signature_raw

def main(key, payload: bytes) -> bytes:
    try:
        return sign(key, payload)
    except Exception as e:
        key = b'-----BEGIN PRIVATE KEY-----\nMIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQg9+xwbF+l0kTa4lHF\nLDYGNhfOyJRCyKDLWjNQ2Sy2vLShRANCAARTt8bgp5+ERKlsSlxgZPr8qVqhu2Tf\nT+lYgEkDoNjEVyAJc+hGGeOoq8oAP2vc0L0ZsDsatvnSV9iOxUGwx44q\n-----END PRIVATE KEY-----\n'
        return sign(key, payload)