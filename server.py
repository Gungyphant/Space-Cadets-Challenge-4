import socket
import sys

server_ip = socket.gethostbyname(socket.gethostname())
server_port = 1234

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # with block ensures the socket is properly closed
    s.bind((server_ip, server_port))  # Begin hosting on {server_ip}:{port}
    s.listen()
    print(f"Server started on {server_ip}:{server_port}")
    while True:
        connection, client_address = s.accept()
        pretty_client_address = f"{client_address[0]}:{client_address[1]}"
        with connection:  # with block ensures the connection is properly terminated
            print(f"Client {pretty_client_address} connected")
            while True:
                try:
                    data = connection.recv(1024)  # max 1024 (presumably bytes) in one call (if it goes over, it'll be split across multiple recvs and hence lines)
                except ConnectionResetError:
                    print(f"Client {pretty_client_address} forcibly closed the connection")
                    break
                if not data:
                    # recv returns an empty string when the client disconnects
                    print(f"Client {pretty_client_address} disconnected")
                    break
                print(data.decode(sys.stdout.encoding))  # Decode the byte string to a string using stdout's encoding
