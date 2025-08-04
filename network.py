import sys
import queue
import multiaddr
import trio

from libp2p import new_host
from libp2p.custom_types import TProtocol
from libp2p.network.stream.net_stream import INetStream
from libp2p.peer.peerinfo import info_from_p2p_addr

PROTOCOL_ID = TProtocol("/chat/1.0.0")
MAX_READ_LEN = 2**32 - 1

OUTGOING_QUEUE = queue.Queue()
INCOMING_QUEUE = queue.Queue()


async def read_data(stream: INetStream) -> None:
    buffer = bytearray()

    async def safe_read(n):
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
            # Read 4-byte length prefix
            length_bytes = await safe_read(4)
            expected_len = int.from_bytes(length_bytes, "big")
            print(f"Expecting {expected_len} bytes")

            # Read the rest of the data
            data = await safe_read(expected_len)
            print(f"Received {len(data)} bytes")
            INCOMING_QUEUE.put(data)

        except Exception as e:
            print(f"error: {e}")
            break



async def write_data(stream: INetStream) -> None:
    MAX_CHUNK = 60000

    while True:
        try:
            data = OUTGOING_QUEUE.get_nowait()
            total_len = len(data)
            length_header = total_len.to_bytes(4, "big")

            await stream.write(length_header)
            print(f"Sending {total_len} bytes in chunks...")

            offset = 0
            while offset < total_len:
                chunk = data[offset:offset + MAX_CHUNK]
                await stream.write(bytes(chunk))
                print(f"Chunk of {len(chunk)} bytes")
                offset += len(chunk)

            print("Write complete")
        except queue.Empty:
            await trio.sleep(0.1)
        except Exception as e:
            print(f"error: {e}")
            break






async def run(port: int, destination: str) -> None:
    listen_addr = multiaddr.Multiaddr(f"/ip4/127.0.0.1/tcp/{port}")
    host = new_host()

    async def stream_handler(stream: INetStream) -> None:
        print("🔌 [stream_handler] new stream accepted")
        async with trio.open_nursery() as nursery:
            nursery.start_soon(read_data, stream)
            nursery.start_soon(write_data, stream)

    host.set_stream_handler(PROTOCOL_ID, stream_handler)

    async with host.run(listen_addrs=[listen_addr]), trio.open_nursery() as nursery:
        if not destination:
            # Server
            print("\nWaiting for incoming connection...")
            print(
                "Run this from the same folder in another console:\n"
                f"    python main.py -d {host.get_addrs()[0]}\n"
            )
        else:
            # Client
            maddr = multiaddr.Multiaddr(destination)
            info = info_from_p2p_addr(maddr)

            await host.connect(info)
            print(f"Connected to peer {info.addrs[0]}")

            stream = await host.new_stream(info.peer_id, [PROTOCOL_ID])

            nursery.start_soon(read_data, stream)
            nursery.start_soon(write_data, stream)

        # Keep running
        await trio.sleep_forever()
