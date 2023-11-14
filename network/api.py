import json
import queue
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from threading import Event
from queue import Queue
from socket import socket, AF_INET, SOCK_STREAM

class Transaction(BaseModel):
    sender: str
    receiver: str
    amount: float
    signature: str
    Nonce: int

class Block(BaseModel):
    Index: int
    Timestamp: int
    Transactions: List[Transaction]
    previousHash: str
    Hash: str

app = FastAPI()
block_queue = Queue()
block_created_event = Event()

@app.get('/') 
def root():
    return {"Api": "V1"}

# Ruta para la operación POST que recibe un bloque y retorna un mensaje de éxito
@app.post("/crear_bloque")
async def crear_bloque(bloque: Block):
    if bloque is None:
        return '400'
    else:
        # Envía el bloque al otro archivo Python
        block_json = json.dumps(bloque.model_dump())
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(('127.0.0.1',5000))
        client.sendall(block_json.encode('utf-8'))
        client.close()
        return '200'

if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=4000)
