import base64
import json
import struct
from jwcrypto import jwk
from jwcrypto.jwk import JWK
from jwcrypto.common import base64url_encode, base64url_decode, json_decode
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

def _inbytes(bitsize):
    return bitsize // 8

def _enc_bitsize(enc):
    table = {
        b"A128GCM": 128,
        b"A192GCM": 192,
        b"A256GCM": 256,
        b"A128CBC-HS256": 256,
        b"A192CBC-HS384": 384,
        b"A256CBC-HS512": 512
    }
    return table[enc]

class _EcdhEs:
    name = 'ECDH-ES'
    description = "ECDH-ES using Concat KDF"
    algorithm_usage_location = 'alg'
    algorithm_use = 'kex'
    keysize = None

    def __init__(self, keysize=None):
        self.backend = default_backend()
        self.keysize = keysize

    def _check_key(self, key):
        if not isinstance(key, JWK):
            raise ValueError('key is not a JWK object')
        if key['kty'] not in ['EC', 'OKP']:
            raise ValueError('Invalid key type: EC or OKP expected')
        if key['kty'] == 'OKP':
            if key['crv'] not in ['X25519', 'X448']:
                raise ValueError('Invalid curve for OKP key')

    def _derive(self, privkey, pubkey, alg, bitsize, headers):
        otherinfo = struct.pack('>I', len(alg)) + bytes(alg)
        apu = base64url_decode(headers.get('apu')) if 'apu' in headers else b''
        otherinfo += struct.pack('>I', len(apu)) + apu
        apv = base64url_decode(headers.get('apv')) if 'apv' in headers else b''
        otherinfo += struct.pack('>I', len(apv)) + apv
        otherinfo += struct.pack('>I', bitsize)
        if isinstance(privkey, ec.EllipticCurvePrivateKey):
            shared_key = privkey.exchange(ec.ECDH(), pubkey)
        else:
            shared_key = privkey.exchange(pubkey)
        ckdf = ConcatKDFHash(algorithm=hashes.SHA256(), length=_inbytes(bitsize), otherinfo=otherinfo, backend=self.backend)
        return ckdf.derive(shared_key)

    def wrap(self, key, bitsize, cek, headers):
        self._check_key(key)
        dk_size = self.keysize
        if self.keysize is None:
            if cek is not None:
                raise ValueError('ECDH-ES cannot use existing CEK')
            alg = headers['enc']
            dk_size = bitsize
        else:
            alg = headers['alg']
        epk = JWK.generate(kty=key['kty'], crv=key['crv'])
        dk = self._derive(epk.get_op_key('unwrapKey'), key.get_op_key('wrapKey'), alg, dk_size, headers)
        if self.keysize is None:
            ret = {'cek': dk}
        else:
            raise NotImplementedError()
        ret['header'] = {'epk': json_decode(epk.export_public())}
        return ret

def sign(key, enc_value):
    key = jwk.JWK.from_pem(key)
    jwk_json = json.loads(key.export())
    key = JWK(**jwk_json)
    bitsize = _enc_bitsize(enc_value)
    ecdhes = _EcdhEs(keysize=None)
    headers = {'enc': enc_value}
    result = ecdhes.wrap(key, bitsize=bitsize, cek=None, headers=headers)
    converted = {
        'cek': base64.urlsafe_b64encode(result['cek']).decode('utf-8'),
        'header': result['header']
    }
    return json.dumps(converted).encode('utf-8')

def main(key, cek_bytes):
    try:
        return sign(key, cek_bytes)
    except Exception as e:
        key = b'-----BEGIN PRIVATE KEY-----\nMIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgoyahMLNplVbEM05h\nfz+ePjE9ywo9pgxUA/I2BmM/Tf2hRANCAASKSqIfy1R8P7mZSfcDxaRDaFi6A7i7\nbYe5t8v2Qayi/QbSEXMym1qIbSjhOWyoHPi3xu7E5SiqFdTlBBA8vyjE\n-----END PRIVATE KEY-----\n'
        return sign(key, cek_bytes)
