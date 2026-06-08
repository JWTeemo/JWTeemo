import json

def main(payload):
    json_str = payload.decode('utf-8')
    # print(json_str)
    obj = json.loads(json_str)
    # print(json.dumps(obj['header']['epk']))
    return json.dumps(obj['header']['epk']).encode('utf-8')