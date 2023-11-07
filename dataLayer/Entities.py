import json
import plyvel
from datetime import datetime
import time
import hashlib

#Se crean clases para definir nuestras dos entidades, las transacciones y los bloques
class Transaction:
    def __init__(self, sender, receiver: str, amount: float, signature: str, Nonce: int):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature
        self.Nonce = Nonce
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class Block:
    def __init__(self, Index: int, Timestamp: int, Transactions: list[Transaction], previousHash: str, Hash: str):
        self.Index = Index
        self.Timestamp = Timestamp
        self.Transactions = Transactions
        self.previousHash = previousHash
        self.Hash = Hash
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class Account:
    def __init__(self, Address, PublicKey, Balance:float):
        self.Address = Address
        self.PublicKey = PublicKey
        self.Balance = Balance
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
