from config import db
from datetime import datetime
from pymongo import MongoClient

import socket

client = MongoClient(f"mongodb://{db["user"]}:{db["pass"]}@localhost:{db["port"]}/")

def db_insert(data):
    db = client["JWTFuzz"]
    collection = db["Records"]
    result = collection.insert_one(data)
    print(f"Inserted ID: {result.inserted_id}")

def interact_with_harness(IP, PORT, jwt_token):
    try:
        sock = socket.create_connection((IP, PORT))
        sock.sendall(jwt_token + b"\n")
        response = sock.recv(1024).decode().strip()
        sock.close()
        return response

    except Exception as e:
        print(jwt_token)
        print(f"Error: {e}")