import socket
import threading as t
import time
import os
address = ("127.0.0.1", 64444)
option = False
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(address)



while option == False:   
    print("type '/login username password' to log in")
    print("type '/signup username password' to sign in")
    selection = input("$")    
    cliente.send(selection.encode('ascii'))
    option = True
    os.system("cls")
    break
 
def recibir_msg():
    while True:
        try:
            message = cliente.recv(1024).decode('ascii')
            print(message)
        except:
            print("Conexion terminada")
            cliente.close()
            break
        
def enviar_msg():
    while True:
        mensaje = input('')
        cliente.send(mensaje.encode('ascii'))


receive_thread = t.Thread(target=recibir_msg)
receive_thread.start()

write_thread = t.Thread(target=enviar_msg)
write_thread.start()
