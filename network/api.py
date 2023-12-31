import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
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

class Account(BaseModel):
    Address: str
    PublicKey: str
    Balance: float

app = FastAPI()

@app.get('/') 
def root():
    import socket
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return {
        "Api": "V1",
        "ip": ip_address
        }

# Ruta para la operación POST que recibe un bloque y retorna un mensaje de éxito
@app.post("/crear_bloque")
async def crear_bloque(bloque: Block):
    if bloque is None:
        return '400'
    else:
        # Envía el bloque al otro archivo Python
        block_json = json.dumps(bloque.model_dump())
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(('172.17.0.3',5000))
        client.sendall(block_json.encode('utf-8'))
        client.close()
        return '200'
    
@app.post('/Create_Account')
async def Create_Account(account: Account):
    print(account)
    if account is None:
        return '400'
    else:
        # Envía la cuenta al otro archivo Python
        account_json = json.dumps(account.model_dump())
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(('172.17.0.3',5000))
        client.sendall(account_json.encode('utf-8'))
        client.close()
        return '200'


if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=4000)
