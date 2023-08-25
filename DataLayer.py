import plyvel
from datetime import datetime
import time
import hashlib

#Se crean clases para definir nuestras dos entidades, las transacciones y los bloques
class Transaction:
    def __init__(self, sender, recipient: str, amount: float):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

class Block:
    def __init__(self, Index: int, Timestamp: int, Transactions, previousHash: str, Hash: str, Nonce: int):
        self.Index = Index
        self.Timestamp = Timestamp
        self.Transactions = Transactions
        self.previousHash = previousHash
        self.Hash = Hash
        self.Nonce = Nonce

#Para generar un bloque necesitamos hacer un hash asi que se crean dos funciones
#generateBlock que agarra siertos parametros y crea el objeto de hash retornando este
#calculateHash que agarra el bloque creado anteriormente y le asigna su hash
def generateBlock(index: int, previousHash: str, Transactions, Nonce: int):
    tiempo_actual = datetime.now()
    tiempo_unix = int(time.mktime(tiempo_actual.timetuple()))
    block = Block(index, tiempo_unix, Transactions, previousHash, "", Nonce)
    block.Hash = calculateHash(block)
    return block
    
def calculateHash(b):
    data = f"{b.Index}{b.Timestamp}{b.previousHash}{b.Nonce}"
    for tx in b.Transactions:
        data += f"{tx.sender}{tx.recipient}{tx.amount}"    
    h = hashlib.sha256()
    h.update(data.encode('utf-8'))

    return h.hexdigest()
    

# Crear una instancia de Block y Transaction para prueba
transactions = [Transaction("Alice", "Bob", 10.0), Transaction("Bob", "Charlie", 5.0)]
block = generateBlock(1, "lala", transactions, 1)

# Calcular y mostrar el hash
print("Hash del bloque:", block.Hash)