import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from threading import Event
from queue import Queue

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
    # Puedes realizar operaciones adicionales aquí si es necesario
    block_queue.put(bloque)
    cola_lista = list(block_queue.queue)
    print(cola_lista)
    block_created_event.set()
    return "Bloque recibido con éxito"

if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=4000)
