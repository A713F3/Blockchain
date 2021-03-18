import socket
import threading

class Client:
    def __init__(self,nick):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.money = 5

        self.keep =  True
        self.nick = nick

        self.lock = threading.Lock() 
    
    """
        Start a connection with server
    """
    def start(self):
        try:
            self.client.connect(("192.168.1.25", 55555))
            print("Connected to the Server!")

        except Exception:
            print("Connection Error!")
            self.stop()
        
        # Starting a thread for receiving messages from server
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        # Starting a thread for sending messages to server
        write_thread = threading.Thread(target=self.write)
        write_thread.start()

    """
        Stop connection
    """
    def stop(self):
        self.keep = False
        self.client.close()

    """
        For sending messages to server
    """
    def write(self):
        while self.keep:
            receiver = input("Receiver> ")
            if receiver == "__q__":
                self.stop()
                break

            amount = input("Amount> ")    
            if amount == "__q__":
                self.stop()
                break  

            data = "{}-{}:{}".format(self.nick, receiver, amount)     

            try:    
                self.client.send(data.encode("ascii"))
            except Exception:
                print("Failed to send data to server")

            print("Send: {}".format(data))

    """
        For receiving messages from server
    """
    def receive(self):
        while self.keep:
            
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.nick.encode('ascii'))
                else:
                    print(message)
            except:
                # Close Connection When Error
                print("An error occured!")
                self.stop()
                break

            

name = input("Enter name: ")

client = Client(name)

client.start()

