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

def findCommand(s, user):
    
    s1 = s.decode('ascii')
    #print(s1)
    #print(s)
    if s1[0] == "/":
        #print("hola")
        cmd = s1.split()[0].lstrip("/")
        #print(cmd)
        msg = s1.split(cmd , 1)[1].lstrip()
        #print(msg)
        if cmd == "broadcast":
            broadcast(msg.encode('ascii'), user)
        if cmd == "servermsg":
            servermsg(msg, user)
        if cmd == "whisper":
            destinatary = msg.split()[0].lstrip()
            content = msg.split(destinatary, 1)[1].lstrip()
            whisper(destinatary, content.encode('ascii'), user)
    else:
        return broadcast(s, user)
    
    
def handle(client):
    while True: 
        try:
            message = client.recv(1024)
            index = clientes.index(client)
            username = usuarios[index]
            
            #broadcast(message)
            findCommand(message, username)
        except:
            index = clientes.index(client)
            clientes.remove(client)
            client.close()
            username = usuarios[index]
            broadcast('{} se ha desconectado!'.format(username).encode('ascii'), "SERVIDOR")
            usuarios.remove(username)
            break

def broadcast(msg, user):
     for client in clientes:
          cadena = user + ": " + msg.decode('ascii')
          client.send(cadena.encode('ascii'))

def servermsg(msg, user):
    print("(SERVER-DM) Mensaje a servidor: {} ", format((msg)))

def whisper(destinatary, msg, user):
    cadena = user + ": " + msg.decode('ascii')
    c_index = usuarios.index(destinatary)
    c = clientes[c_index]
    c.send(cadena.encode('ascii'))

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
                broadcast("{} Se ha unido!".format(username).encode('ascii'), "Servidor")
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
                broadcast("{} Se ha unido!".format(username).encode('ascii'), "SERVIDOR")
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




