# Proyect-Blockchain
Integrantes del grupo: Tomás Arancibia - Guillermo Martínez - Benjamín Ojeda

## Instrucciones:

* Clonar el repositorio
* Hacer ``` pip install -r requerement.txt  ```
* Hacer ``` python3 main.py  ```

## Desarrollo
En esta sección se explicará con mayor detalle la lógica del codigo que se escribió para realizar el proyecto:

* Entities.py: En este archivo se definen dos clases importantes para construir un blockchain, Transaction y Block.
  
  La clase "Transaction" representa la transacción de un blockchain y posee cuatro atributos:
  
  * sender: representa a la persona que envía una transacción.
  * receiver: representa a la persona que recibe la transacción, puede ser su dirección id o algún otro nombre que sirva de referencia.
  * amount: indica la cantidad de recursos que se estan enviando en la transacción, por ejemplo, criptomonedas.
  * Nonce: este número es utilizado por la minería de bloques y se utiliza para asegurar que una transacción no se haga mas de una vez.

    Luego se utiliza la libreria json de pyhtonn para exportar dicha transacción en un formato json
  
  La clase "Block" representa a los bloques, los cuáles son una estructura fundamental para los blockchain ya que, permite organizar y almacenar las transacciones y otros datos de manera segura y eficiente, sus atributos son:
  
  * Index: representa el número que identifica al bloque y sirve para que los demás bloques puedan reconocerse entre ellos, dicho número suele representar la posición del bloque.
  * Timestap: registro de tiempo que indica el momento en el que se creo el bloque.
  * Transactions: representa una lista o alguna otra estructura con las transacciones realizadas por el bloque
  * previousHash: contiene el hash que representa el bloque anterior en la cadena
  * Hash: representa el hash únnico que tiene el bloque.

  De igual forma que la transacción dichos datos se mapean en un formato json especial.

* Store.py: Este código está relacionado con la manipulación de bloques y operaciones de almacenamiento y recuperación en un blockchain

  * generateBlock: Esta función crea un bloque utilizando los parámetros dados, index, previousHash y Transaction, esto lo logra gracias a la clase creada en Entities.py.
  * calcularHash: Simplemente se encarga de calcular el hash del bloque (Concatena el índice, la marca de tiempo, el hash del bloque anterior y los datos de cada transacción y luego le aplica SHA256 retornando un valor en hexadecimal).
  * saveBlock: Esta función se encarga de guardar un bloque en una base de datos, para esto se utiliza Plyvel, la cuál convierte el bloque a formato json usando "toJson" de la clase Block.
  * getBlock: Esta función recibe como parámetro la llave de un bloque y retorna el bloque en formato json
  * getBlocks: Obtiene todos los bloques de la base de datos y los guarda en una lista, luego imprime cada bloque.

* AuthKey.py: Éste código genera una clave pública y privada para una dirección Ethereum utilizando una semilla mnemotécnica (mnemonic phrase).

* main.py: Éste código demuestra como se crean las transacciones, se calculan los hashes, se almacenan y recuperan bloques en una cadena de bloques básica utilizando las funciones definidas en los módulos Store.py, Entities.py y AuthKey.py. Específicamente en dicho archivo se están generando dos bloques de forma estática, en donde el primer bloque es hardcodeado y el segundo bloque se usa para comprobar el funcionamiento.
