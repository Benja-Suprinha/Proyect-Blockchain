import json
from socket import socket, AF_INET, SOCK_STREAM

def recibir_bloque():
    # Creamos un socket TCP
    servidor = socket(AF_INET, SOCK_STREAM)

    # Escuchamos en el puerto especificado
    servidor.bind(("127.0.0.1", 5000))
    servidor.listen()

    while True:
        # Aceptamos una conexión
        cliente, _ = servidor.accept()

        # Leemos el bloque JSON
        bloque_json = cliente.recv(1024).decode("utf-8")

        # Convertimos el bloque JSON a un objeto Python
        bloque = json.loads(bloque_json)

        # Realizamos operaciones con el bloque
        print(bloque)

if __name__ == "__main__":
    recibir_bloque()
