import random
from socket import *
import threading

# Function to handle each client connection
def handleClient(clientSocket, addr):
    try:
        print(f"Connected to client at {addr}")

        while True:
            # Receive message from the client and decode it
            msg = clientSocket.recv(1024).decode()
            if not msg:
                print("null message object received")
                break

            # Convert message to uppercase
            msg = msg.upper()

            # Send the modified message back to the client
            clientSocket.send(msg.encode())

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
