import random
from socket import *
import threading
import json

# Function to handle each client connection
def handleClient(clientSocket, addr):
    try:
        print(f"Connected to client at {addr}")
        wickets = 0
        runs = 0
        while True:
            # Receive message from the client and decode it
            randNum = str(clientSocket.recv(1024), 'utf8')
            if not randNum:
                print("null message object received")
                break
            clientNum = int(randNum)
            randomNum = random.randint(1, 6)
            if randomNum == clientNum:
                wickets += 1
            else:
                runs += clientNum
            

            obj = {
                'runs': runs,
                'wickets': wickets
            }

            reply = json.dumps(obj)

            # Send the reply back to the client
            clientSocket.send(reply.encode('utf-8'))
            if wickets == 10:
                print("all team is out")
                break

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the client socket
        clientSocket.close()
        print(f"Connection with client at {addr} is closed")

# Create a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind the socket to a specific address and port
serverSocket.bind(('', 12000))

# Set the socket to listen for incoming connections
serverSocket.listen()

print("The server is ready to receive requests!")

try:
    while True:
        # Accept incoming connection and get the client socket and address
        clientSocket, addr = serverSocket.accept()

        # Create a new thread to handle the client
        clientThread = threading.Thread(target=handleClient, args=(clientSocket, addr))
        clientThread.start()

except KeyboardInterrupt:
    print("Server stopped")

finally:
    # Close the server socket
    serverSocket.close()
