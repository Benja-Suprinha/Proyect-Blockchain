import json
import plyvel
from datetime import datetime
import time
import hashlib
import Entities

#Para generar un bloque necesitamos hacer un hash asi que se crean dos funciones
#generateBlock que agarra ciertos parametros y crea el objeto de hash retornando este
#calculateHash que agarra el bloque creado anteriormente y le asigna su hash
def generateBlock(index: int, previousHash: str, Transactions):
    tiempo_actual = datetime.now()
    tiempo_unix = int(time.mktime(tiempo_actual.timetuple()))
    block = Entities.Block(index, tiempo_unix, Transactions, previousHash, "")
    block.Hash = calculateHash(block)
    return block
    
def calculateHash(block):
    data = f"{block.Index}{block.Timestamp}{block.previousHash}"
    for tx in block.Transactions:
        data += f"{tx.sender}{tx.receiver}{tx.amount}"    
    h = hashlib.sha256()
    h.update(data.encode('utf-8'))

    return h.hexdigest()
    
def saveBlock(block):
    db = plyvel.DB('./mydb', create_if_missing=True)
    block_data = block.toJSON()
    if block_data is None:
        return "Block no data"
    
    key = bytearray(f"block-{block.Index}", "utf-8").__str__()
    key = key.encode("utf-8")

    err = db.put(key, block_data.encode("utf-8"))
    if err is not None:
        db.close()
        return err

    db.close()
    return 'Block add succefully'


#ahora quiero extraer el valor de un bloque sabiendo su llave, para ello se utilizara la funcion get


def getBlock(key):
    try:
        # accedo a la base de datos
        db = plyvel.DB('./mydb', create_if_missing=True)
        #asigno una variable valor (lo que quiero buscar)
        key = bytearray(f"block-{key}", "utf-8").__str__()
        value = db.get(key.encode('utf-8'))
        #Si existe, lo retorno
        if value is not None:
            return value.decode('utf-8')
        #caso contrario, retorno error
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        #finalmente, cierro la conexion con la db
    finally:
        db.close()

def getBlocks():
    try:
        blockList = []
        db = plyvel.DB('./mydb')
        for key, value in db:
            print(value.decode('utf-8'))
            blockList.append(value.decode('utf-8'))
        return blockList
        db.close()
    except Exception as e:
        print(f"Error: {e}")