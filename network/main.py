import argparse
import sys

import multiaddr
import trio
import libp2p
from socket import socket, AF_INET, SOCK_STREAM
from libp2p.peer.peerinfo import info_from_p2p_addr
from libp2p.typing import TProtocol
from libp2p.network.stream.net_stream_interface import INetStream
from libp2p.crypto.secp256k1 import create_new_key_pair

PROTOCOL_ID = TProtocol("/test/1.0.0")

async def _echo_stream_handler(stream: INetStream) -> None:
    # Wait until EOF
    req = await stream.read()
    res = 'Si estas conectado!'
    print('Se conecto alguien')
    print('Aca hay que pasarle los bloques que ya existen!')
    print(req.decode())
    await stream.write(res.encode())
    await stream.close()

async def read_data(stream: INetStream) -> None:
    while True:
        read_bytes = await stream.read()
        if read_bytes is not None:
            read_string = read_bytes.decode()
            if read_string != "\n":
                # Green console colour: 	\x1b[32m
                # Reset console colour: 	\x1b[0m
                print("\x1b[32m %s\x1b[0m " % read_string, end="")


async def write_data(stream: INetStream) -> None:
    async_f = trio.wrap_file(sys.stdin)
    while True:
        line = await async_f.readline()
        await stream.write(line.encode())

async def run(port: int, destination:str):
    localhost_ip = '127.0.0.1'
    listen_addr = multiaddr.Multiaddr(f"/ip4/0.0.0.0/tcp/{port}")

    host = libp2p.new_host()
    async with host.run(listen_addrs = [listen_addr]):

        print(f'Yo soy {host.get_id().to_string()}')

        if not destination:
            host.set_stream_handler(PROTOCOL_ID, _echo_stream_handler)
            print('Esperando conexiones ... ')
            await trio.sleep_forever()
        else:
            maddr = multiaddr.Multiaddr(destination)
            info = info_from_p2p_addr(maddr)
            print(info.peer_id.to_string())
            await host.connect(info)

            stream = await host.new_stream(info.peer_id, [PROTOCOL_ID])
            msg = f"nodo {host.get_id().pretty()} conectado!"
            msg = 'Se creo un nuevo bloque!'
            msg = msg.encode()

            await stream.write(msg)
            await stream.close()
            response = await stream.read()
            print('Sincronizando ...')
            print(msg.decode())
            print(response.decode())

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

def main() -> None:
    description = """
    Conexion simple de nodos usando una red p2p
    """
    example_maddr = (
        "/ip4/127.0.0.1/tcp/8000/p2p/QmQn4SwGkDZKkUEpBRBvTmheQycxAHJUNmVEnjA2v1qe8Q"
    )
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-p", 
        '--port',
        default=8000, 
        type=int, 
        help='Numero de puerto'
    )
    parser.add_argument(
        '-d',
        "--destination",
        type=str,
        help=f'multiaddres de destino, ejemplo {example_maddr}'
    )
    args = parser.parse_args()
    print(args)

    if not args.port:
        raise RuntimeError('no hay puerto')
    
    try:
        trio.run(run, args.port, args.destination)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()