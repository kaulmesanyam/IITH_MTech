import socket
import random
import json

# Define the server address and port
server_addr = ('127.0.0.1', 12000)

# Get the number of balls you want to play
balls = int(input("Total balls to play: "))

# Create a TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client.connect(server_addr)
    print("Connection established with server")

    while balls > 0:
        for ball in range(1, balls + 1):
            wickets = 0
            if wickets == 10:
                print("all team is out")
                break

            clientNum = random.randint(1, 6)
        
            # Send runs to the server
            client.sendall(bytes(str(clientNum), 'utf8'))

            # Set a timeout for receiving a response from the server
            client.settimeout(1.0)
            while True:
                try:
                    # Try to receive a response from the server
                    responseObj = client.recv(1024).decode('utf-8')
                    response = json.loads(responseObj)
                    # Print score
                    print(f'Response received from {server_addr}: After ball- {ball}: {response}')
                    wickets = response.get('wickets', None)
                    break  # Exit the inner loop on successful response

                except socket.timeout:
                    # Handle the case where the response times out
                    print(f'response from Ball {ball} has timed out -- re-transmitting same packet again')

        exit = "yes"

        if exit.lower() == 'yes':
            break
        else:
            pings = int(input("Total balls to play: "))

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the client socket
    client.close()
    print("Connection closed")
