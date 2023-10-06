import json
import plyvel
from datetime import datetime
import time
import hashlib

#Para generar un bloque necesitamos hacer un hash asi que se crean dos funciones
#generateBlock que agarra ciertos parametros y crea el objeto de hash retornando este
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

#ahora quiero extraer el valor de un bloque sabiendo su llave, para ello se utilizara la funcion get


def getBlockValue(db, key):
    try:
        # accedo a la base de datos
        db = plyvel.DB('./mydb', create_if_missing=True)
        #asigno una variable valor (lo que quiero buscar)
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

