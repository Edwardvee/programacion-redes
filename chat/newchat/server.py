import socket
import threading
import mysql.connector as mysql
import sys

conexiones = []

class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal


    def __str__(self):
        return str(self.id) + " " + str(self.address)
    

    def run(self):
        print("1")
        while self.signal:
            print("2")
            try: 
                print("3")
                data = self.socket.recv(32)
            except: 
                print("El cliente " + str(self.address) + " se desconecto.")
                self.signal = False
                conexiones.remove(self)
            if data != "":
                print("4")
                print("Se recibio algo de " + self.address)         
                print("ID:" + str(self.id) + ": " + str(data.decode("utf-8")))
                for clientes in conexiones:
                    print("5")
                    print("hola")
                    if clientes.id != self.id:
                        clientes.socket.sendall(data)



def newConnections(socket):
        while True:
            sock, address = socket.accept()
            print("Nueva conexion")
            print(sock)
            print(address)
            client = Client(sock, address, len(conexiones), "Nombre", True)
            client_thr = threading.Thread(target=client.run)
            client_thr.start()
            conexiones.append(client)
            
            

def main():
        server = ("127.0.0.1", 62332)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(server)
        s.listen(5)
        newConnectionsThread = threading.Thread(target=newConnections, args=(s,))
        newConnectionsThread.start()
        newConnectionsThread.join()

        print("Escuchando...")

main()



