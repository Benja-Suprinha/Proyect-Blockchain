# Archivo productor.py

from queue import Queue
import threading
import time

def productor():
    while True:
        queue = Queue()
        message = "Hola, mundo!"
        queue.put(message)
        time.sleep(1)

if __name__ == "__main__":
    t = threading.Thread(target=productor)
    t.daemon = True
    t.start()

    time.sleep(5)
    queue = Queue()
    print(queue.get())
