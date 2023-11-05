import json
from mnemonic import Mnemonic
import eth_account
import ecdsa
from ecdsa.keys import SigningKey
import plyvel
import Entities

def Keys():
    #Asi se creo el mnemonic
    #mnemonic = Mnemonic("english").generate()

    mnemonic = 'because transfer reward onion marble casual person protect apology century clip cross'
    #print(mnemonic)
    eth_account.Account.enable_unaudited_hdwallet_features()
    private_key = eth_account.Account.from_mnemonic(mnemonic)._private_key.hex()
    address = eth_account.Account.from_key(private_key).address
    
    private_key = private_key.lstrip("0x")
    private_key = bytes.fromhex(private_key)
    sk = SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)

    public_key = sk.get_verifying_key().to_string("compressed").hex()
    public_key = '0x' + public_key
    genesis_account = Entities.Account(address,public_key,10000000)
    SaveAccount(genesis_account)

    return private_key, public_key, address

def CreateAccount():
    #Asi se creo el mnemonic
    mnemonic = Mnemonic("english").generate()
    #print(mnemonic)
    eth_account.Account.enable_unaudited_hdwallet_features()
    private_key = eth_account.Account.from_mnemonic(mnemonic)._private_key.hex()
    address = eth_account.Account.from_key(private_key).address
    
    private_key = private_key.lstrip("0x")
    private_key = bytes.fromhex(private_key)
    sk = SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)

    public_key = sk.get_verifying_key().to_string("compressed").hex()
    public_key = '0x' + public_key
    private_key = '0x' + private_key.hex()

    account = Entities.Account(address, public_key, 10000)
    SaveAccount(account)

    print("the mnemonic is: ", mnemonic)
    print("the private key is:",private_key)
    print("the public key is:", public_key)
    print("the address is:", address)
    print("Remember to save your private key and the mnemonic")



def SaveAccount(account:Entities.Account):
    db = plyvel.DB('./Accounts', create_if_missing=True)
    account_data = account.toJSON()
    if account_data is None:
        return 'Account no data'
    key = bytearray(f"account-{account.Address}","utf-8").__str__()
    key = key.encode("utf-8")

    err = db.put(key, account_data.encode("utf-8"))
    if err is not None:
        db.close()
        return err
    
    db.close()
    return 'Account create success'

def GetAccounts():
    try:
        accountList = []
        db = plyvel.DB('./Accounts', create_if_missing=True)
        for key, value in db:
            print(value.decode('utf-8'))
            accountList.append(value.decode('utf-8'))
        db.close()
        return accountList
    except Exception as e:
        print(f"Error: {e}")

def GetGenesisAccount():
    db = plyvel.DB('./Accounts')
    key = bytearray(f"account-0x390A3d59E5F689134B7Fc85bBFCeEE05264fDaD8", "utf-8").__str__()
    value = db.get(key.encode('utf-8'))
    if value is not None:
        return value.decode('utf-8')
    else:
        return None
    