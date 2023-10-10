# Proyect-Blockchain
Integrantes del grupo: Tomás Arancibia - Guillermo Martínez - Benjamín Ojeda

## Introducción:

## Desarrollo
En esta sección se explicará con mayor detalle la lógica del codigo que se escribió para realizar el proyecto:

* Entities.py: En este archivo se definen dos clases importantes para construir un blockchain, Transaction y Block.
  
  ```
  class Transaction:
    def __init__(self, sender, receiver: str, amount: float, Nonce: int):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.Nonce = Nonce
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
  ```
  
  Esta clase representa la transacción de un blockchain y posee cuatro atributos:
  
  * sender: representa a la persona que envía una transacción.
  * receiver: representa a la persona que recibe la transacción, puede ser su dirección id o algún otro nombre que sirva de referencia.
  * amount: indica la cantidad de recursos que se estan enviando en la transacción, por ejemplo, criptomonedas.
  * Nonce: este número es utilizado por la minería de bloques y se utiliza para asegurar que una transacción no se haga mas de una vez.

    Luego se utiliza la libreria json de pyhtonn para exportar dicha transacción en un formato json
    
 ```
class Block:
    def __init__(self, Index: int, Timestamp: int, Transactions, previousHash: str, Hash: str):
        self.Index = Index
        self.Timestamp = Timestamp
        self.Transactions = Transactions
        self.previousHash = previousHash
        self.Hash = Hash
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
  ```
  
  Esta clase representa a los bloques, los cuáles son una estructura fundamental para los blockchain ya que, permite organizar y almacenar las transacciones y otros datos de manera segura y eficiente, sus atributos son:
  
  * Index: representa el número que identifica al bloque y sirve para que los demás bloques puedan reconocerse entre ellos, dicho número suele representar la posición del bloque.
  * Timestap: registro de tiempo que indica el momento en el que se creo el bloque.
  * Transactions: representa una lista o alguna otra estructura con las transacciones realizadas por el bloque
  * previousHash: contiene el hash que representa el bloque anterior en la cadena
  * Hash: representa el hash únnico que tiene el bloque.

  De igual forma que la transacción dichos datos se mapean en un formato json especial.
