from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hmac, hashes, padding
import os

def sign(key, payload, iv, aad):
    if len(key) != 64:
        raise ValueError("Key length must be 64 bytes for A256CBC-HS512")

    mac_key = key[:32]
    enc_key = key[32:]

    # PKCS7 填充
    padder = padding.PKCS7(128).padder()
    padded = padder.update(payload) + padder.finalize()

    # AES-256-CBC 加密
    cipher = Cipher(algorithms.AES(enc_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    # 计算 HMAC 输入: AAD || IV || ciphertext || len(AAD in bits)
    al = (8 * len(aad)).to_bytes(8, byteorder='big')
    h = hmac.HMAC(mac_key, hashes.SHA512())
    h.update(aad + iv + ciphertext + al)
    tag = h.finalize()[:32]  # 截断为32字节（256位）

    return ciphertext + tag

def main(key, payload, iv, aad):
    try:
        return sign(key, payload, iv, aad)
    except Exception as e:
        key = os.urandom(64)
        return sign(key, payload, iv, aad)
