import random
from socket import *
import threading

def handleClient(clientSocket, addr):
    try:
        print(f"Connected to client at {addr}")

        while True:
        
            msg = clientSocket.recv(1024).decode()
            if not msg:
                print("null message object received")
                break

            msg = msg.upper()

            clientSocket.send(msg.encode())

    except Exception as e:
        print(f"Error: {e}")

    finally:
        clientSocket.close()
        print(f"Connection with client at {addr} is closed")

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 12000))
serverSocket.listen()

print("The server is ready to receive requests!")

try:
    while True:
        clientSocket, addr = serverSocket.accept()
        clientThread = threading.Thread(target=handleClient, args=(clientSocket, addr))
        clientThread.start()

except KeyboardInterrupt:
    print("Server stopped")

finally:
    serverSocket.close()