import socket
import threading

class Client:
    def __init__(self,nick):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.keep =  True
        self.nick = nick

        self.lock = threading.Lock() 

    def receive(self):
        while self.keep:
            #self.lock.acquire()
            try:
                message = self.client.recv(1024).decode('ascii')
                print(message)

            except:
                print("An error occured!")
                self.client.close()
                break
            #self.lock.release()

    def write(self):
        while self.keep:
            message = input("\n >")

            if message == "__q__":
                self.stop()

            message = "{}: {}".format(self.nick, message)
            self.client.send(message.encode("utf-8"))

    def start(self):
        try:
            self.client.connect(("192.168.1.26", 55555))
            print("Connected to the Server!")
        except:
            print("Connection Error!")
            self.stop()
        
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

    def stop(self):
        self.keep = False
        self.client.close()

name = input("Enter name: ")

client = Client(name)

client.start()

    
##Syncronise receive before write so ">" doesn't overlaps
