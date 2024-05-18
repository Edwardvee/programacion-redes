import socket as s
import threading as t
import sys
PORT = 64444
HOST = "127.0.0.1"

conexiones = []

class Client(t.Thread):
    def __init__(self, socket, address, id, name, signal):
        t.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal

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
            client_thr = t.Thread(target=client.run)
            client_thr.start()
            conexiones.append(client)
            
            

def main():
        server = ("127.0.0.1", 62332)
        socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        socket.bind(server)
        socket.listen(5)
        newConnectionsThread = t.Thread(target=newConnections, args=(s,))
        newConnectionsThread.start()
        newConnectionsThread.join()

        print("Escuchando...")

main()


