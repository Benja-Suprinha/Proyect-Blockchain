import json
import plyvel
from datetime import datetime
import time
import hashlib
import Entities
import ecdsa
from ecdsa.keys import SigningKey
import requests

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
    
def saveBlock(block:Entities.Block):
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
            #print(value.decode('utf-8'))
            blockList.append(value.decode('utf-8'))    
        db.close()
        return blockList
    except Exception as e:
        print(f"Error: {e}")

def generateTransaction(sender: str, receiver: str, amount: float, privateKey: str, nonce: int):
    senderValid = getAddress(sender)
    receiverValid = getAddress(receiver)
    if senderValid is None:
        return 1
    if  receiverValid is None:
        return 1
    senderAmount = getAmount(sender)
    if senderAmount is None:
        return 2
    senderAmount = float(senderAmount)
    amount = float(amount)
    if amount > senderAmount:
        return 2
    
    senderPublicKey = getPublicKey(sender)

    isvalid = isValid(privateKey,senderPublicKey)

    if isvalid is False:
        return 3

    setAmount(receiver,amount)
    transaction = Entities.Transaction(sender,receiver,amount,privateKey,nonce)
    return transaction

def getAddress(address: str):
    try:
        db = plyvel.DB('./Accounts')
        key = bytearray(f'account-{address}',"utf-8").__str__()
        value = db.get(key.encode('utf-8'))
        if value is not None:
            return value.decode('utf-8')
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")

def getAmount(address: str):
    try:
        db = plyvel.DB('./Accounts')
        key = bytearray(f'account-{address}',"utf-8").__str__()
        value = db.get(key.encode('utf-8'))
        if value is not None:
            value = json.loads(value)
            amount = value['Balance']
            return amount
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")

def setAmount(address: str, amount: float):
    try:
        db = plyvel.DB('./Accounts')
        key = bytearray(f'account-{address}', 'utf-8').__str__()
        key = key.encode('utf-8')
        value = db.get(key)
        value = json.loads(value)
        value['Balance'] = value['Balance'] + amount
        value = json.dumps(value)
        err = db.put(key, value.encode('utf-8'))
        if err is not None:
            db.close()
            return err
        return 200
    except Exception as e:
        print(f'Error: {e}')
    finally:
        db.close()

def getPublicKey(address: str):
    try:
        db = plyvel.DB('./Accounts')
        key = bytearray(f'account-{address}',"utf-8").__str__()
        value = db.get(key.encode('utf-8'))
        if value is not None:
            value = json.loads(value)
            amount = value['PublicKey']
            return amount
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")

def isValid(privateKey, publicKey):
    if len(privateKey) != 66:
        return False
    
    private_key = privateKey.lstrip("0x")
    private_key = bytes.fromhex(private_key)
    sk = SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)

    public_key = sk.get_verifying_key().to_string("compressed").hex()
    public_key = '0x' + public_key
    if public_key == publicKey:
        return True
    else:
        return False