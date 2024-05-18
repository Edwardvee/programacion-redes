import socket as s
import threading as t
import mysql
from sqlfunctions import Database
import _mysql_connector
import sys
PORT = 64444
HOST = "127.0.0.1"




def RecibirMsg(s):
    while True:
        recieved_msg = s.recv(1024)
        print(f"Servidor: {recieved_msg!r}")
            

def EnviarMsg(s):
    while True:
        send_msg = input("Tu:")   
        if send_msg != "adios":
            s.send(send_msg.encode())
            print(f"Cliente: {send_msg}")
        else: 
            s.send(send_msg.encode())
            print(f"Cliente: {send_msg}")

def main():
    socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    try:
        print("conectando")
        socket.connect((HOST, PORT))
    except: 
        print("no se pudo conectar al servidor")   
        sys.exit()
    try:
        




           
           