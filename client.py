import socket
import threading
import time
from tkinter import *
from tkinter import ttk


def transmit_message(message, connection):
    connection.sendall(message.encode())  # Encode the message as bytes and transmit it to the server

def gui(connection, client_name: str):
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()

    chat_area = ttk.Label(frm)
    chat_area.grid(row=0)

    user_name = ttk.Label(frm, text=f"{client_name}: ")
    user_name.grid(column=0, row=1)

    message_box = Text(frm)
    message_box.grid(column=1, row=1)

    send_button = Button(text="Send", command=lambda: transmit_message(message_box.get('1.0', 'end-1c'), connection))
    send_button.grid(column=2, row=1)

    def live_update_chat_area():
        try:
            while True:
                chat = connection.recv(1024).decode()
                # If the connection sends twice between receives, the data may be duplicated
                # However, the message should be preceded by \0, so the message is everything after the last \0
                chat = chat.split("\0")[-1]
                # print(chat)
                chat_area.config(text=chat)
                time.sleep(0.1)
        except ConnectionAbortedError, OSError:
            pass

    chat_update_thread = threading.Thread(target=live_update_chat_area)
    chat_update_thread.start()

    root.mainloop()


def communicate(server_ip: str, server_port: str, client_name: str) -> None:
    server_port = int(server_port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:  # with block ensures the socket is properly closed
        try:
            connection.connect((server_ip, server_port))  # Connect to the server
        except ConnectionRefusedError as e:
            raise ConnectionRefusedError(f"{server_ip}:{server_port} refused the connection; is it running?") from e
        # Exchange important information
        server_name = connection.recv(1024).decode()
        connection.sendall(client_name.encode())

        gui(connection, client_name)

        # print(f"Successfully connected to {server_name}")
        # while True:
        #     message = input("> ")
        #     if message == "!quit":
        #         break
        #     connection.sendall(message.encode())  # Encode the message as bytes and transmit it to the server
    print(f"Successfully disconnected from {server_name}")

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
