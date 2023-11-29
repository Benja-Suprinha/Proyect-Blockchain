# Proyect-Blockchain
Integrantes del grupo: Tomás Arancibia - Guillermo Martínez - Benjamín Ojeda

## Instrucciones:
* En primera instancia, se recuerda que debe tener instalado Docker en su equipo, ya que el montaje de las red se hace utilizando contenedores.
  * Paso 1: Clonar el repositorio
* Ahora, se pasa a montar la red (API y nodos)
* Paso 2: Montaje de la API
  * Desde el root del proyecto
  * Hacer ```docker build -t api-chain -f ./dockerfile-api . ```
  * Hacer ```docker run --name api-chain -p 4000:4000 -it api-chain ```
  * Verificar en localhost:4000 que figura la ip: 172.17.0.2 (en caso de no salir dicha ip, reiniciar docker y repetir).
* Paso 3: Montaje del primer nodo (nodo maestro)
  * Desde el root del proyecto
  * Hacer ```docker build -t net-chain -f ./dockerfile-network .```
  * Hacer ```docker run -p 5000:5000 --name master-node -it net-chain ```
  * Verificar abriendo el archivo "dockerfile-network-node", en la linea 35 se debe cambiar el parametro que va luego del -d por el que figura en consola al ejecutar el comando anterior.
* Paso 4: Montaje del segundo nodo (nodo ligth)
  * Desde el root del proyecto
  * Hacer ```docker build -t node-chain -f ./dockerfile-network-node . ```
  * Hacer ```docker run --name ligth-node -it node-chain ```
* Luego de montar la red y verificar que funciona correctamente, se pasa a montar la app.
* Paso 5: montaje de la app
  * Desde la ruta /dataLayer
  * Hacer ```docker build -t app-chain -f ./dockerfile . ```
  *  ```docker run --name app-chain -it app-chain ```
  *  Verificar que se vea lo siguiente:
  * ![image](https://github.com/Benja-Suprinha/Proyect-Blockchain/assets/135309866/e2d26b21-c01c-45cf-a93f-6453c1d89b59)

 

