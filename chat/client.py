import socket as s
import threading as t
import sys
PORT = 64444
HOST = "127.0.0.1"

socket = s.socket(s.AF_INET, s.SOCK_STREAM)

with socket:
        socket.connect((HOST, PORT))
        while True:
            def RecibirMsg():
                recieved_msg = socket.recv(1024)
                print(f"Servidor: {recieved_msg!r}")
                if recieved_msg == b"adios":
                     sys.exit()

                     return

            def EnviarMsg():
                send_msg = input("Tu:")   
                if send_msg != "adios":
                    socket.send(send_msg.encode())
                    print(f"Cliente: {send_msg}")
                else: 
                    socket.send(send_msg.encode())
                    print(f"Cliente: {send_msg}")
                    socket.close()
                    sys.exit()

                    return

            rcvthread = t.Thread(target=RecibirMsg, daemon=True)
            sendthread = t.Thread(target=EnviarMsg, daemon=True)
            rcvthread.start()
            sendthread.start()
           
           
           