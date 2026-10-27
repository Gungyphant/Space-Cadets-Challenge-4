import socket

def communicate(server_ip: str, server_port: str, client_name: str) -> None:
    server_port = int(server_port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # with block ensures the socket is properly closed
        try:
            s.connect((server_ip, server_port))  # Connect to the server
        except ConnectionRefusedError as e:
            raise ConnectionRefusedError(f"{server_ip}:{server_port} refused the connection; is it running?") from e
        # Exchange important information
        server_name = s.recv(1024).decode()
        s.sendall(client_name.encode())

        print(f"Successfully connected to {server_name}")
        while True:
            message = input("> ")
            if message == "!quit":
                break
            else:
                s.sendall(message.encode())  # Encode the message as bytes and transmit it to the server
    print(f"Successfully disconnected from {server_ip}:{server_port}")

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    help_message = f"error: The command-line arguments should either be of the form \"ip port name\" or \"ip:port name\""
    match len(args):
        case 0:
            # Get them from input
            server_ip = input("Server IP: ")
            server_port = input("Server port: ")
            client_name = input("Client name: ")
        case 1:
            # ip:port
            if ":" not in args[0]:
                print(help_message)
                quit()
            server_ip, server_port = args[0].split(":")
            client_name = input("Client name: ")
        case 2:
            # ip port or ip:port name
            if ":" in args[0]:
                server_ip, server_port = args[0].split(":")
                client_name = args[1]
            else:
                server_ip, server_port = args
                client_name = input("Client name: ")
        case 3:
            # ip port name
            server_ip, server_port, client_name = args
        case _:
            print(help_message)
            quit()
    communicate(server_ip, server_port, client_name)
