import socket
import threading

class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(("192.168.1.26", 55555))

        self.clients = []

        self.keep = True

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while self.keep:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                self.clients.remove(client)
                client.close()

                break

    def receive(self):
        while self.keep:
            client, adress = self.s.accept()

            print(f"{adress} is connected.")

            self.clients.append(client)

            handle_thread = threading.Thread(target=self.handle, args=(client,))
            handle_thread.start()
            
    def start(self):
        self.s.listen()

        print("Server is listening...")

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()  

    def stop(self):
        self.keep = False  
        self.s.close()

server = Server()

server.start()