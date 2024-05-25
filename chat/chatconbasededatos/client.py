import socket as s
import threading as t
import mysql
from sqlfunctions import Database
#import _mysql_connector
import sys
import os

option = False
selection = 0
while option == False:   
    print("1. Iniciar sesión")
    print("2. Crear sesión")
    selection = input("Ingrese un numero: ")
    if selection == "1" or selection == "2":
        option = True
        break
    else:
        option = False
        os.system('cls')
        print("Numero invalido")


cliente = s.socket(s.AF_INET, s.SOCK_STREAM)
cliente.connect(('127.0.0.1', 64444))

if selection == "1":
    os.system('cls')
    print("Iniciando sesion...")
    cliente.send(selection.encode('ascii'))
    username = input("Nombre de usuario: ")
    cliente.send(username.encode('ascii'))
    password = input("Contraseña: ")
    cliente.send(password.encode('ascii'))
    os.system('cls')
if selection == "2":
    os.system('cls')
    print("Creando cuenta...")
    cliente.send(selection.encode('ascii'))
    username = input("Nombre de usuario: ")
    cliente.send(username.encode('ascii'))
    password = input("Contraseña: ")
    cliente.send(password.encode('ascii'))
    os.system('cls')
    

def recibir_msg():
    while True:
        try:
            message = cliente.recv(1024).decode('ascii')
            if message == 'NICK':
                cliente.send(username.encode('ascii'))
            else:
                print(message)
        except:
            
            print("Error de conexion")
            cliente.close()
            break
        
def enviar_msg():
    while True:
        mensaje = '{}: {}'.format(username, input(''))
        cliente.send(mensaje.encode('ascii'))

receive_thread = t.Thread(target=recibir_msg)
receive_thread.start()

write_thread = t.Thread(target=enviar_msg)
write_thread.start()



           
           