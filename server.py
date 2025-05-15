import socket
import threading
import time

class Server:
    def __init__(self, host='127.0.0.1', port=9000):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start_server(self):
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(3)
            print(f'\nSERVER IS LISTENING ON {self.host}:{self.port}')
            self.client, addr = self.server.accept()
            print(f'[CONNECTED]: {addr}')
            self.chat_loop()
        except KeyboardInterrupt:
            print('\n[SERVER SHUTDOWN]')
        finally:
            self.server.close()

    def send_message_server(self):
        while True:
            try:
                message = input('[SERVER MESSAGE]: ')
                self.client.sendall(message.encode())
            except (BrokenPipeError, ConnectionResetError, OSError):
                print('[ERROR]: Client disconnected.')
                break

    def receive_message_server(self):
        while True:
            try:
                response = self.client.recv(1024).decode()
                if response:
                    print(f'\n[CLIENT MESSAGE]: {response}')
                else:
                    print('[INFO]: Client disconnected.')
                    break
            except (ConnectionResetError, OSError):
                print('[ERROR]: Connection lost.')
                break

    def chat_loop(self):
        threading.Thread(target=self.receive_message_server, daemon=True).start()
        threading.Thread(target=self.send_message_server, daemon=True).start()
        while True:
            time.sleep(1)


class Client:
    def __init__(self, host='127.0.0.1', port=9000):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_client(self):
        try:
            self.client.connect((self.host, self.port))
            print(f'[CONNECTED]')
            self.chat_loop()
        except KeyboardInterrupt:
            print('\n[CLIENT SHUTDOWN]')
        except ConnectionRefusedError:
            print('[ERROR]: Cannot connect to server.')
        finally:
            self.client.close()

    def send_message_client(self):
        while True:
            try:
                message = input('[YOUR MESSAGE]: ')
                self.client.sendall(message.encode())
            except (BrokenPipeError, ConnectionResetError, OSError):
                print('[ERROR]: Server disconnected.')
                break

    def receive_message_client(self):
        while True:
            try:
                response = self.client.recv(1024).decode()
                if response:
                    print(f'[SERVER MESSAGE]: {response}')
                else:
                    print('[INFO]: Server closed the connection.')
                    break
            except (ConnectionResetError, OSError):
                print('[ERROR]: Connection lost.')
                break

    def chat_loop(self):
        threading.Thread(target=self.receive_message_client, daemon=True).start()
        threading.Thread(target=self.send_message_client, daemon=True).start()
        while True:
            time.sleep(1)


def chose_mode():
    try:
        mode = input('Choose your mode (server/client): ')
        if mode.lower() == 'server':
            s = Server()
            s.start_server()
        elif mode.lower() == 'client':
            c = Client()
            c.start_client()
        else:
            print('[ERROR]: Invalid mode.')
    except KeyboardInterrupt:
        print('\n[EXIT]')

chose_mode()


    

