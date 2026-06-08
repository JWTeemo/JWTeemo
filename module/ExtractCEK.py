import base64
import json

def main(json_data):
    # print(json_data)
    d = json.loads(json_data)
    cek_bytes = base64.urlsafe_b64decode(d['cek'] + '==')  # 注意 padding
    # print(cek_bytes)  # 输出原始 bytes
    return cek_bytes
