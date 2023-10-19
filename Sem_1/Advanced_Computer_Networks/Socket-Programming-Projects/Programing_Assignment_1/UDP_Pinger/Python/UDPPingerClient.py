import socket
import time

# Define the server address and port
server_addr = ('127.0.0.1', 12000)

# Get the number of pings to send from the user
pings = int(input("Number of pings to send: "))

# Create a UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialize variables to track round-trip times (rtt) and lost packets
rtt = []
lost_packets = 0

# Iterate over the range of sequence numbers (1 to pings)
for seq_no in range(1, pings + 1):
    # Get the current timestamp for RTT calculation
    timestamp = time.time()

    # Construct the message in the format 'ping sequence_number timestamp'
    message = f'ping {seq_no} {timestamp}'

    # Send the message to the server using UDP
    client.sendto(message.encode(), server_addr)

    # Set a timeout for receiving a response from the server
    client.settimeout(1.0)

    try:
        # Try to receive a response and the server address
        response, server_addr = client.recvfrom(1024)

        # Calculate the round-trip time (RTT)
        curr_rtt = time.time() - timestamp
        rtt.append(curr_rtt)

        # Print the response and RTT
        print(f'response received from {server_addr}: {response.decode()} | RTT: {curr_rtt:.6f} seconds')

    except socket.timeout:
        # Handle the case where the response times out
        print(f'Ping {seq_no} has timed out')
        lost_packets += 1

# Close the UDP socket
client.close()

# Calculate and print statistics if any responses were received
if rtt:
    min_rtt = min(rtt)
    max_rtt = max(rtt)
    avg_rtt = sum(rtt) / len(rtt)
    loss_rate = (lost_packets / pings) * 100
    print("\nStatistics:\n")
    print(f"  Packets sent: {pings}")
    print(f"  Packets received: {pings - lost_packets}")
    print(f"  Packets lost: {lost_packets} ({loss_rate:.2f}% loss)")
    print(f"  Minimum RTT: {min_rtt:.6f} seconds")
    print(f"  Maximum RTT: {max_rtt:.6f} seconds")
    print(f"  Average RTT: {avg_rtt:.6f} seconds")
else:
    print("\nNo response received as all packets got lost")
