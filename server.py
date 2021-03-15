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

    """
        Start Server
    """
    def start(self):
        self.s.listen()

        print("Server is listening...")

        # Start a thread for accepting clients
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()  

        # Start a thread for server commands
        command_thread = threading.Thread(target=self.commands(), args=())
        command_thread.start()
    
    """
        Stop Server
    """
    def stop(self):
        pickle.dump(self.adresses, open( "clients.p", "wb" ))
        self.keep = False  
        self.s.close()

        self.keep = True

    """
        Broadcast message to a client
    """
    def broadcast(self, message, client):
        try:
            client.send(message)
        except:
            print("Broadcast Error!")

        # For broadcasting a message to every client
        #for client in self.clients:
        #    client.send(message)

    """
        Handle each clients messages
    """
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
    
    """
        Accept clients to server
    """
    def receive(self):
        while self.keep:
            # Accept client
            client, adress = self.s.accept()
            
            # If client is known
            if client in self.clients: 
                print(f"{self.adresses[adress]} is connected")
            else:
                print(f"{adress} is connected.")

                self.clients.append(client)
                self.adresses[adress] = "--"
            
            # After aceepting client to start a thread for messages
            handle_thread = threading.Thread(target=self.handle, args=(client,adress))
            handle_thread.start()

    """
        For server commands
    """      
    def commands(self):
        command = input()

        if command == "q":
            self.stop()

if __name__ == "__main__":
    server = Server()
    server.start()