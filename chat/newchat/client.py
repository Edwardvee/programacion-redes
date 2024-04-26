import socket
import threading
import mysql.connector as mysql
import sys


def rcv(s):
  while True:
    try:
      data = s.recv(1024)
    except: 
      print("No se recibio ningun msj")
    if data != "":
     print(data.decode("utf-8"))

def send(s): 
  while True:
    try:
      msj = input("Tu:")
    except:
      print("error")
    if msj != "":
      s.send(msj.encode())
    else: 
      print("El mensaje esta vacio")


def main():
  server = ("127.0.0.1", 62332)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(server)

  mainThread = threading.Thread(target=rcv, args=(s,))    
  mainThread.start()
  send(s)
            
main()
