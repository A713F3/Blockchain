import socket
import threading
import pickle

class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(("192.168.1.26", 55555))

        try:
            self.adresses = pickle.load(open("clients.p", "rb"))
            self.clients = []
        
        except:
            self.clients = []
            self.adresses = {}

        self.keep = True

    def broadcast(self, message, client):
        try:
            client.send(message)
        except:
            print("Broadcast Error!")

        #for client in self.clients:
        #    client.send(message)

    def handle(self, client, adress):
        while self.keep:
            try:
                message = client.recv(1024)
                self.broadcast(message, client)
                if message[:2] == b'::':
                    self.adresses[adress] = message[2:]

                print(f"{self.adresses[adress]} {message}")
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
                print(f"{self.adresses[adress]} is connected")
            else:
                print(f"{adress} is connected.")

                self.clients.append(client)
                self.adresses[adress] = "--"
            

            handle_thread = threading.Thread(target=self.handle, args=(client,adress))
            handle_thread.start()
            
            
    def start(self):
        self.s.listen()

        print("Server is listening...")

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()  

        command_thread = threading.Thread(target=self.commands(), args=())
        command_thread.start()

    def stop(self):
        pickle.dump(self.adresses, open( "clients.p", "wb" ))
        self.keep = False  
        self.s.close()

server = Server()

server.start()