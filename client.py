import socket

def communicate(server_ip: str, server_port: str):
    server_port = int(server_port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # with block ensures the socket is properly closed
        try:
            s.connect((server_ip, server_port))  # Connect to the server
        except ConnectionRefusedError as e:
            raise ConnectionResetError(f"{server_ip}:{server_port} refused the connection; is it running?")
        print(f"Successfully connected to {server_ip}:{server_port}")
        while True:
            message = input("> ")
            if message == "!quit":
                break
            else:
                s.sendall(message.encode())  # Encode the message as bytes and transmit it to the server
    print(f"Successfully disconnected from {server_ip}:{server_port}")

if __name__ == "__main__":
    # import argparse
    # parser = argparse.ArgumentParser()
    # parser.add_argument("server_ip", help="The IP address of the server to connect to")
    # parser.add_argument("server_port", help="The port of the server to connect to")
    # args = parser.parse_args()
    # communicate(args.server_ip, args.server_port)
    import sys
    args = sys.argv[1:]
    help_message = f"error: The command-line arguments should either be of the form \"ip port\" or \"ip:port\""
    match len(args):
        case 0:
            # Get them from input
            server_ip = input("Server IP: ")
            server_port = input("Server port: ")
        case 1:
            # ip:port
            if ":" not in args[0]:
                print(help_message)
                quit()
            server_ip, server_port = args[0].split(":")
        case 2:
            # ip, port
            server_ip, server_port = args
        case _:
            print(help_message)
            quit()
    communicate(server_ip, server_port)
