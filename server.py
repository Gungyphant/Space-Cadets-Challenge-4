import socket
import sys
import argparse
import threading
import time

# class Client:
#     def __init__(self, connection, client_address):
#         self.connection = connection
#         self.client_address = client_address
#
#         self.pretty_client_address = f"{self.client_address[0]}:{self.client_address[1]}"
#         # Exchange important information
#         self.connection.sendall(server_name.encode())
#         self.client_name = connection.recv(1024).decode()
#
#         print(f"Client {self.client_name} ({self.pretty_client_address}) connected")

chat_state = ""


def announce(message: str) -> None:
    global chat_state
    chat_state += message + "\n"


def send_messages(connection: socket.socket):
    try:
        with connection:
            while True:
                connection.sendall(("\0" + chat_state).encode())
                time.sleep(0.1)
    except ConnectionResetError:
        pass


def communicate(connection: socket.socket, client_address):
    pretty_client_address = f"{client_address[0]}:{client_address[1]}"
    # Exchange important information
    connection.sendall(server_name.encode())
    client_name = connection.recv(1024).decode()

    print(f"Client {client_name} ({pretty_client_address}) connected")
    announce(f"{client_name} has joined the server")

    # Begin sending messages (in a separate thread, to prevent blocking while waiting for messages)
    sending_thread = threading.Thread(target=send_messages, args=(connection,))
    sending_thread.start()

    with connection:  # with block ensures the connection is properly terminated
        while True:
            try:
                data = connection.recv(1024)  # max 1024 (presumably bytes) in one call (if it goes over, it'll be split across multiple recvs and hence lines)
            except ConnectionResetError:
                print(f"Client {client_name} ({pretty_client_address}) forcibly closed the connection")
                announce(f"{client_name} has left the server")
                break
            if not data:
                # recv returns an empty byte when the client disconnects
                print(f"Client {client_name} ({pretty_client_address}) disconnected")
                announce(f"{client_name} has left the server")
                break
            message = f"{client_name}: {data.decode(sys.stdout.encoding).replace("\n", "  ")}"  # Decode the byte string to a string using stdout's encoding
            print(message)
            announce(message)


parser = argparse.ArgumentParser()
parser.add_argument("--name", help="the public name for the server")
parser.add_argument("--port", help="the port to host the server on", type=int)
args = parser.parse_args()

server_ip = socket.gethostbyname(socket.gethostname())
if args.port is None:
    server_port = 1234
else:
    server_port = args.port

if args.name is None:
    server_name = f"{server_ip}:{server_ip}"
else:
    server_name = args.name

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # with block ensures the socket is properly closed
    s.bind((server_ip, server_port))  # Begin hosting on {server_ip}:{port}
    s.listen()
    if args.name is None:
        print(f"Server started on {server_ip}:{server_port}")
    else:
        print(f"Server '{server_name}' started on {server_ip}:{server_port}")
    while True:
        threading.Thread(target=communicate, args=s.accept()).start()
