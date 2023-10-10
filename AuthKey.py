from mnemonic import Mnemonic
import eth_account

def Keys():
    #Asi se creo el mnemonic
    #mnemonic = Mnemonic("english").generate()

    mnemonic = 'because transfer reward onion marble casual person protect apology century clip cross'
    print(mnemonic)
    eth_account.Account.enable_unaudited_hdwallet_features()
    public_key = eth_account.Account.from_mnemonic(mnemonic).address
    private_key = eth_account.Account.from_mnemonic(mnemonic).key
    
    print("la llave privada es: ",private_key)
    print("la llave publica es: ",public_key)

    return private_key, public_key