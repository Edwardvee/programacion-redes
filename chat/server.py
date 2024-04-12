import socket as s
import threading as t
import sys
PORT = 64444
HOST = "127.0.0.1"

socket = s.socket(s.AF_INET, s.SOCK_STREAM)

with socket: 
    socket.bind((HOST,PORT))
    socket.listen()
    conn, addr = socket.accept()
    with conn:
        print(f"Conectado a {addr}")
        while True: 
           
            def RecibirMsg():               
                recieved_msg = conn.recv(1024)
                print(f"Cliente: {recieved_msg!r}")
               
                if recieved_msg == b"adios":
                    sys.exit()
                    return
           

            def EnviarMsg():
                send_msg = input("Tu:")
                if send_msg != "adios":
                 conn.sendall(send_msg.encode())
                 print(f"Servidor: {send_msg}")
                else: 
                 conn.sendall(send_msg.encode())
                 print(f"Servidor: {send_msg}")
                 conn.close()
                 sys.exit()
                 return 
                
                 

            rcvthread = t.Thread(target=RecibirMsg, daemon=True)
            sendthread = t.Thread(target=EnviarMsg, daemon=True)
            rcvthread.start()
            sendthread.start()
           
          
           
           
            

    