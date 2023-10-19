import time
from socket import *
import threading

Questions = {
    "a": "a",
    "b": "b",
    "c": "c",
    "d": "d",
    "e": "e"
}

arr = ["a","b","c","d","e"]

PORT = 12001

# Function to handle each client connection
def handleClient(clientSocket, addr):
    score = 0
    try:
        print(f"Connected to client at {addr}")

        while True:
            # Receive message from the client and decode it
            command = clientSocket.recv(1024).decode()
            if not command:
                print("null message object received")
                break

            if command == 'start':

                
                print("quiz started")
                ind = 0
                while True:
                    clientSocket.send(arr[ind].encode())
                    print(f"Question sent: {arr[ind]}")
                    ans = clientSocket.recv(1024).decode()
                    print(f"ans received:  {ans}")
                    if ans == Questions.get(arr[ind], None):
                        print("right answer!")
                        score = score + 1
                    else:
                        print("wrong answer")
                    clientSocket.send(bytes(str(score), 'utf8'))
                    ind = ind + 1
                    if(ind == 5):
                        break
                    time.sleep(1)



            # Send the score back to the client
            

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the client socket
        clientSocket.close()
        print(f"Connection with client at {addr} is closed")

# Create a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind the socket to a specific address and port
serverSocket.bind(('', PORT))

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
