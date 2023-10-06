import json
import plyvel
from datetime import datetime
import time
import hashlib

#Se crean clases para definir nuestras dos entidades, las transacciones y los bloques
class Transaction:
    def __init__(self, sender, receiver: str, amount: float):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class Block:
    def __init__(self, Index: int, Timestamp: int, Transactions, previousHash: str, Hash: str, Nonce: int):
        self.Index = Index
        self.Timestamp = Timestamp
        self.Transactions = Transactions
        self.previousHash = previousHash
        self.Hash = Hash
        self.Nonce = Nonce
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

#Para generar un bloque necesitamos hacer un hash asi que se crean dos funciones
#generateBlock que agarra siertos parametros y crea el objeto de hash retornando este
#calculateHash que agarra el bloque creado anteriormente y le asigna su hash
def generateBlock(index: int, previousHash: str, Transactions, Nonce: int):
    tiempo_actual = datetime.now()
    tiempo_unix = int(time.mktime(tiempo_actual.timetuple()))
    block = Block(index, tiempo_unix, Transactions, previousHash, "", Nonce)
    block.Hash = calculateHash(block)
    return block
    
def calculateHash(block):
    data = f"{block.Index}{block.Timestamp}{block.previousHash}{block.Nonce}"
    for tx in block.Transactions:
        data += f"{tx.sender}{tx.receiver}{tx.amount}"    
    h = hashlib.sha256()
    h.update(data.encode('utf-8'))

    return h.hexdigest()
    
def saveBlock(db, block):
    block_data = block.toJSON()
    if block_data is None:
        return None
    
    key = bytearray(f"block-{block.Index}", "utf-8").__str__()
    key = key.encode("utf-8")

    err = db.put(key, block_data.encode("utf-8"))
    if err is not None:
        return err

    return None

# Crear una instancia de Block y Transaction para prueba
transactions = [Transaction("Alice", "Bob", 10.0), Transaction("Bob", "Charlie", 5.0)]
block = generateBlock(1, "lala", transactions, 1)

# Calcular y mostrar el hash
print("Hash del bloque:", block.Hash)

db = plyvel.DB('./mydb', create_if_missing=True)
print(saveBlock(db,block))
for key, value in db:
    print("Clave:", key, "Valor:", value)
db.close()