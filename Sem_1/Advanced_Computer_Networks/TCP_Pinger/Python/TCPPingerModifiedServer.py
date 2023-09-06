from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('', 12000))
serverSocket.listen()

print("The server is ready to receive requests!")

try:
    clientSocket, addr = serverSocket.accept()
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
    print("Connection closed")