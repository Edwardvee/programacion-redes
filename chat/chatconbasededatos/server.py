import socket as s
import threading as t
import mysql
import time
from sqlfunctions import Database
#import _mysql_connector
import sys
clientes = []
usuarios = []
server = ("127.0.0.1", 64444)
socket = s.socket(s.AF_INET, s.SOCK_STREAM)
socket.bind(server)
socket.listen(5)
        

print("Escuchando...")

def findCommand(s):
    if s[0] == "/":
        cmd = s.split()[0].lstrip("/")
        msg = s.split(cmd , 1)[1].lstrip()
        if cmd == "broadcast":
            broadcast(msg)
        if cmd == "servermsg":
            servermsg(msg)
        if cmd == "whisper":
            destinatary = msg.split()[0].lstrip()
            content = msg.split(destinatary, 1)[1].lstrip()
            whisper(destinatary, content)
    else:
        return broadcast(msg)
    
    
def handle(client):
    while True: 
        try:
            message = client.recv(1024)
            findCommand(message)
        except:
            index = clientes.index(client)
            clientes.remove(client)
            client.close()
            username = usuarios[index]
            broadcast('{} se ha desconectado!'.format(username).encode('ascii'))
            usuarios.remove(username)
            break

def broadcast(msg):
     for client in clientes:
          client.send(msg)

def servermsg(msg):
    print("(SERVER-DM) Mensaje a servidor: {} ", format((msg)))

def whisper(destinatary, msg):
    c_index = usuarios.index(destinatary)
    c = clientes[c_index]
    c.send(msg)

def receive():
    while True:
        client, addr = socket.accept()
        print("Conexion con {}".format(str(addr)))
        selection = client.recv(1024).decode('ascii')
        if selection == "1":
            username = client.recv(1024).decode('ascii')
            password = client.recv(1024).decode('ascii')
            if Database.LogIn(username,password,Database.cursor) != -1:
                usuarios.append(username)
                clientes.append(client)
                print("Nombre de usuario es {}".format(username))
                broadcast("{} Se ha unido!".format(username).encode('ascii'))
                client.send('Conectado al servidor!'.encode('ascii'))
                 # Start Handling Thread For Client
                thread = t.Thread(target=handle, args=(client,))
                thread.start()
            else:
                print("Sesion invalida, cerrando conexion")
                client.send('Usuario no existe! Conectese devuelta y vuelva a intentarlo'.encode('ascii'))
                time.sleep(5)
                client.close()
        if selection == "2":
            username = client.recv(1024).decode('ascii')
            password = client.recv(1024).decode('ascii')
            if Database.SignIn(username,password,Database.cursor, Database.db) != None:
                usuarios.append(username)
                clientes.append(client)
                print("Nombre de usuario es {}".format(username))
                broadcast("{} Se ha unido!".format(username).encode('ascii'))
                client.send('Conectado al servidor!'.encode('ascii'))
                 # Start Handling Thread For Client
                thread = t.Thread(target=handle, args=(client,))
                thread.start()
            else:
                print("Nombre de usuario utilizado, cerrando conexion.")
                client.send('Nombre de usuario utilizado, cerrando conexion.'.encode('ascii'))
                time.sleep(5)
                client.close()
receive()




