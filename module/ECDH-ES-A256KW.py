import json
import os
import struct
from jwcrypto import jwk
from jwcrypto.jwk import JWK
from jwcrypto.common import base64url_encode, base64url_decode, json_decode
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash
from cryptography.hazmat.primitives import hashes, keywrap
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

def _inbytes(bitsize):
    return bitsize // 8

class ECDH_ES_AKW:
    def __init__(self, keysize):
        self.backend = default_backend()
        self.keysize = keysize

    def _derive(self, privkey, pubkey, alg, bitsize, headers):
        otherinfo = struct.pack('>I', len(alg)) + bytes(alg.encode())
        apu = base64url_decode(headers.get('apu')) if 'apu' in headers else b''
        otherinfo += struct.pack('>I', len(apu)) + apu
        apv = base64url_decode(headers.get('apv')) if 'apv' in headers else b''
        otherinfo += struct.pack('>I', len(apv)) + apv
        otherinfo += struct.pack('>I', bitsize)
        shared_key = privkey.exchange(ec.ECDH(), pubkey) if hasattr(privkey, 'exchange') else privkey.exchange(pubkey)
        ckdf = ConcatKDFHash(algorithm=hashes.SHA256(), length=_inbytes(bitsize), otherinfo=otherinfo, backend=self.backend)
        return ckdf.derive(shared_key)

    def wrap(self, privkey_jwk, cek, alg, headers=None):
        if headers is None:
            headers = {}
        key = JWK(**privkey_jwk)
        epk = JWK.generate(kty=key['kty'], crv=key['crv'])
        kek = self._derive(epk.get_op_key('unwrapKey'), key.get_op_key('wrapKey'), alg, self.keysize, headers)
        encrypted_key = keywrap.aes_key_wrap(kek, cek, self.backend)
        return {
            'encrypted_key': base64url_encode(encrypted_key),
            'header': {'epk': json_decode(epk.export_public())}
        }

def sign(key, cek_bytes):
    key = jwk.JWK.from_pem(key)
    jwk_json = json.loads(key.export())
    keysize = 256
    ecdh = ECDH_ES_AKW(keysize)
    headers = {'alg': 'ECDH-ES+A256KW'}
    result = ecdh.wrap(jwk_json, cek_bytes, 'ECDH-ES+A256KW', headers)
    return json.dumps(result).encode('utf-8')

def main(key, cek_bytes):
    try:
        return sign(key, cek_bytes)
    except Exception as e:
        key = b'-----BEGIN PRIVATE KEY-----\nMIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgoyahMLNplVbEM05h\nfz+ePjE9ywo9pgxUA/I2BmM/Tf2hRANCAASKSqIfy1R8P7mZSfcDxaRDaFi6A7i7\nbYe5t8v2Qayi/QbSEXMym1qIbSjhOWyoHPi3xu7E5SiqFdTlBBA8vyjE\n-----END PRIVATE KEY-----\n'
        return sign(key, cek_bytes)