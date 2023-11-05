import Store
import Entities
import AuthKey
import plyvel

private_key, public_key, address = AuthKey.Keys()

# Crear una instancia de Block y Transaction genesis
transactions = [Store.NewTransaction("", address, 10.0, '', 0)]
block = Store.generateBlock(1, "0000000000000000000000000000000000000000000000000000000000000000", transactions)
Store.saveBlock(block)

while True:
    print('Ingrese que quiere hacer')
    print('1 -> Mostrar todos los bloques de la cadena')
    print('2 -> Crear una cuenta')
    print('3 -> Mostrar cuenta genesis')
    print('4 -> Mostrar todas las cuentas')
    print('0 -> salir')
    option = input('> ')
    if(option == '0'):
        break
    if(option == '1'):
        Store.getBlocks()
    if(option == '2'):
        AuthKey.CreateAccount()
    if(option == '3'):
        print(AuthKey.GetGenesisAccount())
    if(option == '4'):
        AuthKey.GetAccounts()