import queue
import multiaddr
import trio
import config as c

from libp2p import new_host
from libp2p.custom_types import TProtocol
from libp2p.network.stream.net_stream import INetStream
from libp2p.peer.peerinfo import info_from_p2p_addr

PROTOCOL_ID = TProtocol("/chat/1.0.0")
MAX_READ_LEN = 2**32 - 1

OUTGOING_QUEUE = queue.Queue()
INCOMING_QUEUE = queue.Queue()
CONNECTION = False


async def read_data(stream: INetStream) -> None:
    buffer = bytearray()

    async def safe_read(n):
        # Read in chunks if necessary
        while len(buffer) < n:
            chunk = await stream.read(MAX_READ_LEN)
            if chunk is None:
                raise EOFError("Connection closed")
            buffer.extend(chunk)
        result = buffer[:n]
        del buffer[:n]
        return result

    while True:
        try:
            # Attempt to read length message once it has been receieved
            length_bytes = await safe_read(4)
            expected_len = int.from_bytes(length_bytes, "big")
            print(f"Expecting {expected_len} bytes")

            # Attempt to read message once it has been receieved
            # Expecting a certain amount of bytes
            data = await safe_read(expected_len)
            print(f"Received {len(data)} bytes")

            # parse the data received
            username_len = int.from_bytes(data[:2], "big")
            username = data[2 : 2 + username_len].decode("utf-8")
            image = data[2 + username_len :]

            print(f"[{username}] Sent image of {len(image)} bytes")

            INCOMING_QUEUE.put((username, image))
        except Exception as e:
            print(f"error: {e}")
            break


async def write_data(stream: INetStream) -> None:
    MAX_CHUNK = 60000

    while True:
        try:
            # When Image as been sent 
            image_bytes = OUTGOING_QUEUE.get_nowait()
            username_bytes = c.USERNAME.encode("utf-8")
            username_len = len(username_bytes)

            # Attach username to beginning of message before sending
            header = username_len.to_bytes(2, "big") + username_bytes
            full_payload = header + image_bytes

            # Specify size of data
            total_len = len(full_payload)
            length_header = total_len.to_bytes(4, "big")

            # Send size of data
            await stream.write(length_header)
            print(f"Sending {total_len} bytes in chunks...")

            offset = 0

            # Chunking data til all bytes have been written
            while offset < total_len:
                chunk = full_payload[offset : offset + MAX_CHUNK]
                await stream.write(chunk)
                offset += len(chunk)

            print("Write complete")
        except queue.Empty:
            await trio.sleep(0.1)
        except Exception as e:
            print(f"error: {e}")
            break


async def run(port: int, destination: str) -> None:
    # Listening Address
    # Set to 127.0.0.1 (all interfaces) at the moment
    listen_addr = multiaddr.Multiaddr(f"/ip4/127.0.0.1/tcp/{port}")
    host = new_host()

    async def stream_handler(stream: INetStream) -> None:
        print("new stream accepted")
        # Connection has been acknowledged on the server side
        global CONNECTION
        CONNECTION = True
        # Both client and server are capable of sending and receiving data now
        async with trio.open_nursery() as nursery:
            nursery.start_soon(read_data, stream)
            nursery.start_soon(write_data, stream)

    # Our T Protocol is passed to the stream_handler
    host.set_stream_handler(PROTOCOL_ID, stream_handler)

    async with (
        host.run(listen_addrs=[listen_addr]),
        trio.open_nursery() as nursery,
    ):
        if not destination:
            # Server
            print("\nWaiting for incoming connection...")
            print(
                "Run this from the same folder in another console (replace python potentially with whatever command you use instead):\n"
                f"    python main.py -d {host.get_addrs()[0]}\n"
            )
        else:
            # Client
            maddr = multiaddr.Multiaddr(destination)
            info = info_from_p2p_addr(maddr)

            await host.connect(info)
            print(f"Connected to peer {info.addrs[0]}")
            # Connection has been acknowledged on the client side
            global CONNECTION
            CONNECTION = True

            stream = await host.new_stream(info.peer_id, [PROTOCOL_ID])

            # Both client and server are capable of sending and receiving data now
            nursery.start_soon(read_data, stream)
            nursery.start_soon(write_data, stream)

        # Keep running
        await trio.sleep_forever()
