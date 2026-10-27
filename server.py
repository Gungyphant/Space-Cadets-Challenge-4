import socket
import sys
import argparse

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
        connection, client_address = s.accept()
        pretty_client_address = f"{client_address[0]}:{client_address[1]}"
        with connection:  # with block ensures the connection is properly terminated
            # Exchange important information
            connection.sendall(server_name.encode())
            client_name = connection.recv(1024).decode()

            print(f"Client {client_name} ({pretty_client_address}) connected")
            while True:
                try:
                    data = connection.recv(1024)  # max 1024 (presumably bytes) in one call (if it goes over, it'll be split across multiple recvs and hence lines)
                except ConnectionResetError:
                    print(f"Client {client_name} ({pretty_client_address}) forcibly closed the connection")
                    break
                if not data:
                    # recv returns an empty string when the client disconnects
                    print(f"Client {client_name} ({pretty_client_address}) disconnected")
                    break
                print(f"{client_name}: {data.decode(sys.stdout.encoding)}")  # Decode the byte string to a string using stdout's encoding
