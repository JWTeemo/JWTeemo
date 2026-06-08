from pathlib import Path
import time
import socket
import random
from generator import DAG
from config import target
from utils import db_insert

def interact_with_harness(PORT, jwt_token):
    try:
        sock = socket.create_connection(("127.0.0.1", PORT))
        sock.sendall(jwt_token + b"\n")
        response = sock.recv(1024).decode().strip()
        sock.close()
        return response
    except Exception as e:
        print(f"Error: {e}")

def Fuzz():
    G = DAG(Path("grammar/jwt.fbnf").read_text())
    cases = 100000
    mutate_pool = []
    for node_name in G.nodes.keys():
        if "value" in node_name or "claim" in node_name:
            mutate_pool.append(node_name)
    for __ in range(cases + 1):
        Mutate_Type = random.choice([0, 1])
        Mutate_Node = random.choice(mutate_pool)
        jwt, records = G.generate("jwt", False, Mutate_Type, Mutate_Node)
        if len(jwt.decode()) > 200000:
            continue
        res = {}
        flag = 0
        for impl in target.keys():
            resp = interact_with_harness(target[impl], jwt)
            res[impl] = resp
            if "FAILED" not in resp:
                flag += 1

        if flag != 0 and flag != len(target.keys()):
            db_insert(res)

        if flag > len(target.keys()) // 2:
            G.selector.valid(records)

if __name__ == "__main__":
    Fuzz()
