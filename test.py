import Store
import Entities
import AuthKey
import plyvel
import json

private_key, public_key, address = AuthKey.Keys()
# Crear una instancia de Block y Transaction para prueba
transactions = [Entities.Transaction("Alice", "Bob", 10.0, private_key)]
block = Store.generateBlock(1, "", transactions)
# Calcular y mostrar el hash
print("Hash del bloque 1:", block.Hash)
print(Store.saveBlock(block))
transactions = [Entities.Transaction("Bob", "Charlie", 5.0, private_key)]
block2 = Store.generateBlock(2, block.Hash, transactions)
print("Hash del bloque 2: ", block2.Hash)
print(Store.saveBlock(block2))
print("Se hace un get al bloque con index 1: ",Store.getBlock(1))
print("Se hace un get a todos los bloques de la cadena")
Store.getBlocks()