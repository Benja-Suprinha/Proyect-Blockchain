import Store
import Entities
import AuthKey
import plyvel
import json

private_key, public_key, address = AuthKey.Keys()
# Crear una instancia de Block y Transaction genesis
transactions = [Entities.Transaction("", address, 10.0, '', 0)]
block = Store.generateBlock(1, "0000000000000000000000000000000000000000000000000000000000000000", transactions)
Store.saveBlock(block)

while True:
    print('----------------------------------------------')
    print('Ingrese que quiere hacer')
    print('1 -> Crear una cuenta')
    print('2 -> Mostrar cuenta genesis')
    print('3 -> Mostrar todas las cuentas')
    print('4 -> Mostrar todos los bloques de la cadena')
    print('5 -> Mostrar el bloque con el index ...')
    print('6 -> Hacer una transaccion')
    print('0 -> salir')
    print('----------------------------------------------')
    option = input('> ')
    print('----------------------------------------------')
    if(option == '0'):
        break
    if(option == '1'):
        AuthKey.CreateAccount()
    if(option == '2'):
        print(AuthKey.GetGenesisAccount())
    if(option == '3'):
        AuthKey.GetAccounts()
    if(option == '4'):
        blockList = Store.getBlocks()
        index = 0
        for block in blockList:
            data = json.loads(block)
            print(block)
            print('----------------------------------------------')
    if(option == '5'):
        index = int(input('Ingrese el index que quiere ver: '))
        print(Store.getBlock(index))
    if(option == '6'):
        sender = input('Ingrese el address del sender: ')
        receiver = input('Ingrese el address del receiver: ')
        amount = input('Ingrese el monto que quiere transferir: ')
        privateKey = input('Ingrese su autenticacion: ')
        print('En proceso ...')
        blockList = Store.getBlocks()
        nonceLastBlock = 0
        indexLastBlock = 0
        previousHash = ''
        for block in blockList:
            data = json.loads(block)
            nonceLastBlock = data['Transactions'][0]['Nonce']
            indexLastBlock = data['Index']
            previousHash = data['Hash']
        index = indexLastBlock + 1
        nonce = nonceLastBlock + 1
        transaction = Store.generateTransaction(sender,receiver,amount,privateKey,nonce)
        if transaction == 1:
            print('Transaccion fallida usuario no encontrado')
        if transaction == 2:
            print('Saldo insuficiente')
        if transaction == 3:
            print('Firma equivocada')
        else:
            transaction = [transaction]
            print('Transaccion generada exitosamente ...')
            print('Generando bloque ...')
            block = Store.generateBlock(index,previousHash,transaction)
            Store.saveBlock(block)
            print('Bloque generado y guardado exitosamente.')