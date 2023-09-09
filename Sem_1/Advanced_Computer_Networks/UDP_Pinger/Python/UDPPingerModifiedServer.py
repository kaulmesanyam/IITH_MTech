from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to socket
serverSocket.bind(('', 12000))
print("server is ready")
while True:
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    print(f"Message received from client - {address}")
    # Capitalize the message from the client
    message = message.upper()
    
    # Send the capitalized message back to the client
    serverSocket.sendto(message, address)
    print(f'response sent back to client - {address}')