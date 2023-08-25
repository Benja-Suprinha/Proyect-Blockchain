import json

class Transaction:
    def __init__(self, sender, receiver: str, amount: float):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __json__(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
        }


class Block:
    def __init__(self, Index: int, Timestamp: int, Transactions, previousHash: str, Hash: str, Nonce: int):
        self.Index = Index
        self.Timestamp = Timestamp
        self.Transactions = []
        self.previousHash = previousHash
        self.Hash = Hash
        self.Nonce = Nonce

    def __json__(self):
        return {
            "Index": self.Index,
            "Timestamp": self.Timestamp,
            "Transactions": [transaction.__json__() for transaction in self.Transactions],
            "previousHash": self.previousHash,
            "Hash": self.Hash,
            "Nonce": self.Nonce,
        }


block = Block(1, 1234567890, [Transaction("Alice", "Bob", 100), Transaction("Bob", "Carol", 200)], "previous hash", "hash", 12345)
json_string = json.dumps(block)