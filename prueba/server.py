#1. Realizar un programa socket server y client de conexion basica que solo envie un string en forma bi direccional ingresado por teclado.

#2. el programa servidor debe tener una lista o diccionario con nombre de usuario y contraseña. cuando el cliente envie "/login username contraseña" el servidor lo debe verificar con el diccionario, imprimir y enviar "bienvenido {nombre de usuario}" o conexion rechazada y cerrar el socket. 

import socket as s
import threading as t
import time

clientes = [] #lista de clientes conectados
usuarios = [] #lista de usuarios conectados
usuarios_dir = [["pepe", "123123"]] #lista de usuarios
server = ("127.0.0.1", 64444)
socket = s.socket(s.AF_INET, s.SOCK_STREAM)
socket.bind(server) #bindeo al socket creado la dupla server
socket.listen(5) #lo pongo a escuchar
        

print("El servidor esta escuchando en el puerto: ")
def handle(client):
    while True: 
        try:
            message = client.recv(1024)  
            index = clientes.index(client) #busco el indice del cliente segun la lista de clientes
            username = usuarios[index] #como se deben enviar al mismo tiempo el indice del nombre de usuario y de cliente deben ser el mismo
            #recibo el  msj
            c_findCommand(message, username)
        except:
            index = clientes.index(client)
            clientes.remove(client)
            client.close() #elimino de la lista de clientes y cierro la conexion
            username = usuarios[index]
            print('{} se ha desconectado!'.format(username))
            broadcast('{} se ha desconectado!'.format(username).encode('ascii'), "SERVIDOR")
            usuarios.remove(username) #elimino de la lista de usuarios conectados
            break


def findCommand(s): #encontrar comandos para el primer mensaje,  estos solo deberian ser login o si<<<up o se cierra la conexion
    s1 = s.decode('ascii') #decodifico a ascii el mensaje en base16 del cliente
    if s1[0] == "/": #busco si el primer caracter del mensaje es un /
        cmd = s1.split()[0].lstrip("/") #determino el comando que se ingreso
        if cmd == "login": #si el comando es login
            username = s1.split(cmd , 1)[1].split(" ")[1].lstrip() #con el split determino nombre y usuario
            password = s1.split(cmd , 1)[1].split(" ")[2].lstrip()
            if login(username, password) == username: 
                return "LogIn" #devuelvo login para marcar que fue exitoso
            if login(username, password) == "en linea":
                return "UsuarioConectado"
            else: 
                return False #un logeo fallido para cerrar la conexion del usuario
        if cmd == "signup": #si el comando es signup
            username = s1.split(cmd , 1)[1].split(" ")[1].lstrip()
            password = s1.split(cmd , 1)[1].split(" ")[2].lstrip()
            if signup(username,password) == True:
                return "LogIn"
            if signup(username,password) == False : return False    
        else:return False #devuelvo falso porque no se envio un comando de estos dos
    else:
        return False #devuelvo falso si el primer mensaje no fue un comando para cerrar la conexion del servidor
    
def s_findCommand():
    while True:
        s = input("$")
        #decodifico a ascii el mensaje en base16 del cliente
        if s[0] == "/": #busco si el primer caracter del mensaje es un /
            cmd = s.split()[0].lstrip("/") #determino el comando que se ingreso
            if cmd == "all": #si el comando es all realizar un broadcast
                broadcast(s.encode('ascii'), "Sevidor")
            if cmd == "users": #si el comando es users, imprimir los usuarios
                print_users("Sevidor")
            if cmd == "ips": #si el comando es ips, imprimir las ips de los clientes
                print_ips("Sevidor")   
            else:return False #devuelvo falso porque no se envio un comando 
        else:
            broadcast(s.encode('ascii'), "Sevidor")

def c_findCommand(s, user):
    s1 = s.decode('ascii') 
    if s1[0] == "/": 
        cmd = s1.split()[0].lstrip("/") #determino el comando que se ingreso
        message = s1.split(cmd, 1)[1].lstrip()
        if cmd == "all": 
            broadcast(message.encode('ascii'), user)
        if cmd == "users":
            print_users(user) 
        if cmd == "ips": 
            print_ips(user)       
        else:return False 
    else:
        print(s.decode('ascii'))




def broadcast(msg, user):
     for client in clientes:
          cadena = user + ": " + msg.decode('ascii')
          client.send(cadena.encode('ascii')) #broadcast simple, envia a todos los clientes


def print_users(user):
    if user != "Sevidor":
        for user in usuarios:
            c_index = usuarios.index(user)
            c = clientes[c_index]
            c.send(user.encode('ascii'))
    else:
        for user in usuarios:
            print(user)

def print_ips(user):
    if user != "Sevidor":
        for client in clientes:
            c_index = usuarios.index(user)
            c = clientes[c_index]
            c.send(client.encode('ascii'))
    else:
        for client in clientes:
            print(client)

def check_user_in_users(username):
    for user in usuarios:
        if user == username:
            return True
    return False

def login(username, password):
    for user in usuarios_dir:
        if user[0] == username and user[1] == password and check_user_in_users(username) == False:
            usuarios.append(username)
            return username
        else:
            return "en linea"
    return False

def signup(username, password): 
    for user in usuarios_dir:
        if user[0] == username:
            return False
    usuarios_dir.append([username, password])
    usuarios.append(username)
    return True
    

def receive():
    while True:
        client, addr = socket.accept()
        print("Conexion con {}".format(str(addr)))
        firstMsg = client.recv(1024)
        if findCommand(firstMsg) == "LogIn":
            clientes.append(client)
            print("Logeado, escuchando...")
            #broadcast("{} Se ha unido!".format(username).encode('ascii'), "Servidor")
            thread = t.Thread(target=handle, args=(client,))
            thread.start()
        elif findCommand(firstMsg) == "UsuarioConectado":    
            client.send('Usuario ya conectado'.encode('ascii'))
            time.sleep(2)
            client.close()
            print("Usuario ya conectado")
            #broadcast("{} Se ha unido!".format(username).encode('ascii'), "Servidor")
            thread = t.Thread(target=handle, args=(client,))
            thread.start()    
        elif findCommand(firstMsg) == False:
            print("Comando invalido")
            client.send('Conexion rechazada o usuario no existe! Conectese devuelta y vuelva a intentarlo'.encode('ascii'))
            time.sleep(1)
            client.close() 
receive()
