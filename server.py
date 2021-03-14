import socket
import threading
import pickle

class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(("192.168.1.26", 55555))

        try:
            self.clients = pickle.load(open("clients.p", "rb"))
            self.clients = pickle.load(open("client_names.p", "rb"))
        except:
            self.clients = []
            self.client_names = []

        self.keep = True

    def broadcast(self, message, client):
        try:
            client.send(message)
        except:
            print("Broadcast Error!")

        #for client in self.clients:
        #    client.send(message)

    def handle(self, client):
        while self.keep:
            try:
                message = client.recv(1024)
                self.broadcast(message, client)
                print(message)
            except:
                self.clients.remove(client)
                client.close()
                break
        
    def commands(self):
        command = input()

        if command == "q":
            self.stop()

    def receive(self):
        while self.keep:
            client, adress = self.s.accept()
            
            if client in self.clients: 
                print(f"{self.adress_names[self.adresses.indexof(adress)]} is connected")
            else:
                print(f"{adress} is connected.")

                self.clients.append(client)
            

            handle_thread = threading.Thread(target=self.handle, args=(client,))
            handle_thread.start()
            
            
    def start(self):
        self.s.listen()

        print("Server is listening...")

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()  

        command_thread = threading.Thread(target=self.commands(), args=())
        command_thread.start()

    def stop(self):
        self.keep = False  
        pickle.dump(self.clients, open( "clients.p", "wb" ))
        pickle.dump(self.client_names, open( "client_names.p", "wb" ))
        self.s.close()

server = Server()

server.start()