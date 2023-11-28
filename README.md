# Proyect-Blockchain
Integrantes del grupo: Tomás Arancibia - Guillermo Martínez - Benjamín Ojeda

## Instrucciones:
* En primera instancia, se recuerda que debe tener instalado Docker en su equipo, ya que el montaje de las red se hace utilizando contenedores.
  * Paso 1: Clonar el repositorio
  * Una vez clonado el repositorio, se pasa a montar la red.
  * Paso 2: Montaje de la red
  * Desde el root del proyecto
  * Hacer ```docker build -t net-chain -f ./dockerfile-network .```
  * Hacer ```docker build -t node-chain -f ./dockerfile-network-node . ```
  * Hacer ```docker build -t api-chain -f ./dockerfile-api . ```
  * Luego, desde la ruta /dataLayer
  * Hacer ```docker build -t app-chain -f ./dockerfile . ```
  * Hacer ```docker run -p 5000:5000 -it net-chain ```
  * Luego, se debe configurar el id del peer
  * Hacer ```docker run -it node-chain ```
  * Hacer ```docker run -it api-chain ```
  * Finalmente, se debe iniciar la app
  * Aquí hay 2 caminos dependiendo del Sistema operativo que se esté utilizando.
  * En el caso de que se utilice Linux, los pasos son los siguientes:
  * 
  * En el caso de que se use Windows/Mac, se deben seguir los siguientes pasos:
  * 

