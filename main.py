import Store
import Entities
import plyvel

# Crear una instancia de Block y Transaction para prueba
transactions = [Entities.Transaction("Alice", "Bob", 10.0, 1)]
block = Store.generateBlock(1, "lala", transactions)
# Calcular y mostrar el hash
print("Hash del bloque:", block.Hash)
print(Store.saveBlock(block))
transactions = [Entities.Transaction("Bob", "Charlie", 5.0, 2)]
block2 = Store.generateBlock(2, block.Hash, transactions)
print(Store.saveBlock(block2))
print(Store.getBlock(1))
Store.getBlocks()