# Archivo consumidor.py

from queue import Queue

def consumidor():
    queue = Queue()

    while True:
        message = queue.get()
        print(message)

if __name__ == "__main__":
    consumidor()
