import socket
import time

# Define the server address and port
server_addr = ('127.0.0.1', 12000)

# Get the number of pings to send from the user
pings = int(input("Number of pings to send: "))

# Create a TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Initialize variables to track round-trip times (rtt) and lost packets
rtt = []
lost_packets = 0
total_packets = 0

try:
    # Connect to the server
    client.connect(server_addr)
    print("Connection established with server")

    while pings > 0:
        for seq_no in range(1, pings + 1):
            timestamp = time.time()
            message = f'ping {seq_no} {timestamp}'

            # Send the message to the server
            client.sendall(message.encode())
            total_packets += 1

            # Set a timeout for receiving a response from the server
            client.settimeout(1.0)
            while True:
                try:
                    # Try to receive a response from the server
                    response = client.recv(1024)

                    # Calculate the round-trip time (RTT)
                    curr_rtt = time.time() - timestamp
                    rtt.append(curr_rtt)

                    # Print the response and RTT
                    print(f'Response received from {server_addr}: {response.decode()} | RTT: {curr_rtt:.6f} seconds')
                    break  # Exit the inner loop on successful response

                except socket.timeout:
                    # Handle the case where the response times out
                    print(f'Ping {seq_no} has timed out -- re-transmitting same packet again')
                    lost_packets += 1
                    total_packets += 1
                    timestamp = time.time()

        if rtt:
            min_rtt = min(rtt)
            max_rtt = max(rtt)
            avg_rtt = sum(rtt) / len(rtt)
            loss_rate = (lost_packets / total_packets) * 100
            print("\nStatistics:\n")
            print(f"  Packets sent: {total_packets}")
            print(f"  Packets received: {total_packets - lost_packets}")
            print(f"  Packets lost: {lost_packets} ({loss_rate:.2f}% loss)")
            print(f"  Minimum RTT: {min_rtt:.6f} seconds")
            print(f"  Maximum RTT: {max_rtt:.6f} seconds")
            print(f"  Average RTT: {avg_rtt:.6f} seconds")
        else:
            print("\nNo response received as all packets got lost\n")

        exit = "yes"

        if exit.lower() == 'yes':
            break
        else:
            pings = int(input("Number of pings to send: "))

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the client socket
    client.close()
    print("Connection closed")
