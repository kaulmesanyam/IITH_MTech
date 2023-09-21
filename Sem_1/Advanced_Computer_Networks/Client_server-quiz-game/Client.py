import socket
import time

# Define the server address and port
PORT = 12001
server_addr = ('127.0.0.1', PORT)


# Get the number of pings to send from the user
pings = int(input("Number of answers to send: "))

# Create a TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Initialize variables to track round-trip times (rtt) and lost packets


try:
    # Connect to the server
    client.connect(server_addr)
    print("Connection established with server")

    start = input("Type - start to begin:  ")
    client.sendall(start.encode())

    for seq_no in range(1, pings + 1):
        ques = client.recv(1024).decode()
        ans = str(input("Answer: "))

        # Send ans to the server
        client.sendall(ans.encode())
        score = client.recv(1024).decode()
        print(f"current score: {score}")


except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the client socket
    client.close()
    print("Connection closed")
