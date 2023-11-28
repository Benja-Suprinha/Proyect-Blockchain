# Proyect-Blockchain
Integrantes del grupo: Tomás Arancibia - Guillermo Martínez - Benjamín Ojeda

## Instrucciones:
* Recomendacion usar linux o wsl
* Para linux/wsl
  * desde el root del proyecto
  * Hacer ``` pip install -r requerement.txt  ``` 
  * Hacer ``` python3 main.py  ```
* Para windows debe tener intalado y abierto docker
  * Clonar el repositorio
  * Ahora, desde el root del proyecto
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

