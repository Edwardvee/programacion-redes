import socket
import threading
import sys

conexiones = []

class Main(threading.Thread):
    def __init__(self, target=Hola):
        server = ("127.0.0.1", 65555)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(server)
        con
        return


    def Hola():
        return

