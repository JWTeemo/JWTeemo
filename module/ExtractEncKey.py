import json

def main(payload):
    json_str = payload.decode('utf-8')
    obj = json.loads(json_str)
    return obj['encrypted_key'].encode('utf-8')