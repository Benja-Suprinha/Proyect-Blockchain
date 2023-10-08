import Store
import Entities
import plyvel

# Crear una instancia de Block y Transaction para prueba
transactions = [Entities.Transaction("Alice", "Bob", 10.0, 1), Entities.Transaction("Bob", "Charlie", 5.0, 2)]
block = Store.generateBlock(1, "lala", transactions)
# Calcular y mostrar el hash
print("Hash del bloque:", block.Hash)
db = plyvel.DB('./mydb', create_if_missing=True)
print(Store.saveBlock(db, block))
for key, value in db:
    print("Clave:", key, "Valor:", value)
db.close()