import json
import sys

sys.path.append('../dataLayer')

import requests
import Store
import Entities
import AuthKey
import plyvel
import json
import argparse
import sys
import argparse
import json
import sys

import multiaddr
import trio
from libp2p import new_host
from libp2p.network.stream.net_stream_interface import INetStream
from libp2p.peer.peerinfo import info_from_p2p_addr
from libp2p.typing import TProtocol
from socket import socket, AF_INET, SOCK_STREAM

PROTOCOL_ID = TProtocol("/test/1.0.0")

async def read_data(stream: INetStream) -> None:
    sincronizar()
    while True:
        read_bytes = await stream.read()
        print(read_bytes.decode())
        data = read_bytes.decode()
        if 'Transactions' in data:
            block = Entities.Block(data['Index'], data['Timestamp'], data['Transactions'], data['previousHash'], data['Hash'])
            print(Store.saveBlock(block))
            data = block.toJSON()
        else:
            if 'Address' in data:
                account = Entities.Account(data['Address'], data['PublicKey'], data['Balance'])
                print(AuthKey.SaveAccount(account))
                data = account.toJSON()
        await trio.sleep(0)


async def write_data(stream: INetStream) -> None:
    async_f = trio.wrap_file(sys.stdin)
    await stream.write('Connected!'.encode())
    #blocks = Store.getBlocks()
    #accounts = AuthKey.GetAccounts()
    #blocks = json.dumps(blocks)
    #accounts = json.dumps(accounts)
    #await stream.write(blocks.encode())
    #await stream.write(accounts.encode())
    while True:
        data = recibir_data()
        if 'Transactions' in data:
            block = Entities.Block(data['Index'], data['Timestamp'], data['Transactions'], data['previousHash'], data['Hash'])
            print(Store.saveBlock(block))
            data = block.toJSON()
        else:
            if 'Address' in data:
                account = Entities.Account(data['Address'], data['PublicKey'], data['Balance'])
                print(AuthKey.SaveAccount(account))
                data = account.toJSON()

        await stream.write(data.encode())
        await trio.sleep(0)

async def run(port: int, destination:str):
    import socket
    localhost_ip = socket.gethostname()
    localhost_ip = socket.gethostbyname(localhost_ip)
        # Obtén la dirección IP privada asociada al nombre del host
    listen_addr = multiaddr.Multiaddr(f"/ip4/0.0.0.0/tcp/{port}")
    host = new_host()
    async with host.run(listen_addrs=[listen_addr]), trio.open_nursery() as nursery:
        
        if not destination:  # its the server

            async def stream_handler(stream: INetStream) -> None:
                #nursery.start_soon(read_data, stream)
                nursery.start_soon(write_data, stream)

            host.set_stream_handler(PROTOCOL_ID, stream_handler)

            print(
                f"/ip4/{localhost_ip}/tcp/{port}/p2p/{host.get_id().pretty()} "
                "on dockerfile-network-node."
            )
            print("Waiting for incoming connection...")

            if AuthKey.GetGenesisAccount() is not None:
                print('Genesis block ya creado!')
            else:
                private_key, public_key, address = AuthKey.Keys()
                # Crear una instancia de Block y Transaction genesis
                transactions = [Entities.Transaction("", address, 10.0, '', 0)]
                block = Store.generateBlock(1, "0000000000000000000000000000000000000000000000000000000000000000", transactions)
                Store.saveBlock(block)
                print('Genesis block creado!')
            
            await trio.sleep_forever()


        else:  # its the client
            maddr = multiaddr.Multiaddr(destination)
            info = info_from_p2p_addr(maddr)
            # Associate the peer with local ip address
            await host.connect(info)
            # Start a stream with the destination.
            # Multiaddress of the destination peer is fetched from the peerstore using 'peerId'.
            stream = await host.new_stream(info.peer_id, [PROTOCOL_ID])

            nursery.start_soon(read_data, stream)
            #nursery.start_soon(write_data, stream)
            print(f"Connected to peer {info.addrs[0]}")
            await trio.sleep(0)


def sincronizar():
    print('Sincronizando...')
    #for block in json.loads(blocks):
    #    Store.saveBlock(block) 
    #for account in json.loads(accounts):
    #    AuthKey.SaveAccount(account)
    print('Done!')

def recibir_data():
    # Creamos un socket TCP
    servidor = socket(AF_INET, SOCK_STREAM)

    # Escuchamos en el puerto especificado
    servidor.bind(("0.0.0.0", 5000))
    servidor.listen()

    # Aceptamos una conexión
    cliente, _ = servidor.accept()

    # Leemos el bloque JSON
    bloque_json = cliente.recv(1024).decode("utf-8")

    # Convertimos el bloque JSON a un objeto Python
    bloque = json.loads(bloque_json)

    cliente.close()
    # Realizamos operaciones con el bloque
    print(bloque)
    return bloque

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