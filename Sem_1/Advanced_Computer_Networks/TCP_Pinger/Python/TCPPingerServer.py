import random
from socket import *

# Create a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind the socket to a specific address and port
serverSocket.bind(('', 12000))

# Set the socket to listen for incoming connections
serverSocket.listen()

print("The server is ready to receive requests!")

try:
    # Accept incoming connection and get the client socket and address
    clientSocket, addr = serverSocket.accept()
    print(f"Connected to client at {addr}")

    while True:
        # Generate a random number between 0 and 11
        randomNum = random.randint(0, 11)

        # Receive a message from the client and decode it
        msg = clientSocket.recv(1024).decode()

        # Check if the received message is null
        if not msg:
            print("null message object received")
            break

        # Convert the message to uppercase
        msg = msg.upper()

        # Simulate packet loss based on random number
        if randomNum < 4:
            continue

        # Send the modified message back to the client
        clientSocket.send(msg.encode())

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the client socket
    clientSocket.close()
    print("Connection closed")
