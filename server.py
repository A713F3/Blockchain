import socket
import threading

class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(("192.168.1.26", 55555))

        self.keep = True

        self.clients = []
        self.names = []

    """
        Start Server
    """
    def start(self):
        self.s.listen()

        self.keep = True

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
        self.keep = False  
        self.s.close()
        
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
    def handle(self, client):
        while self.keep:
            try:
                # Receive message from client and send
                message = client.recv(1024)
                self.broadcast(message, client)

                index = self.clients.index(client)
                print(f"{names[index]}: {message}")

            except:
                index = self.clients.index(client)

                del self.clients[index]
                del self.names[index]

                client.close()
                break
    
    """
        Accept clients to server
    """
    def receive(self):
        while self.keep:
            # Accept client
            client, adress = self.s.accept()

            # Request and get clients name
            client.send('NICK'.encode('ascii'))
            name = client.recv(1024).decode('ascii')

            self.clients.append(client) 
            self.names.append(name)
            
            print(f"{name} connected with: {adress}")
            
            # After aceepting client to start a thread for messages
            handle_thread = threading.Thread(target=self.handle, args=(client,))
            handle_thread.start()

    """
        For server commands
    """      
    def commands(self):
        command = input()

        if command == "q":
            self.stop()
        if command == "clients":
            print(self.clients)
            print(self.names)

if __name__ == "__main__":
    server = Server()
    server.start()