import socket
import time

server_addr = ('127.0.0.1', 12000)

pings = int(input("Number of pings to send: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

rtt = []
lost_packets = 0

try:
    client.connect(server_addr)
    print("connection established with server")

    while(pings > 0):
        for seq_no in range(1, pings + 1):
            timestamp = time.time()
            message = f'ping {seq_no} {timestamp}'

            
            client.sendall(message.encode())

            client.settimeout(1.0)

            try:
                response = client.recv(1024)

                curr_rtt = time.time() - timestamp
                rtt.append(curr_rtt)

                print(f'response received from {server_addr}: {response.decode()} | RTT: {curr_rtt:.6f} seconds')

            except socket.timeout:
                print(f'Ping {seq_no} has timed out')
                lost_packets = lost_packets + 1

        if rtt:
            min = min(rtt)
            max = max(rtt)
            avg = sum(rtt) / len(rtt)
            loss_rate = (lost_packets / pings) * 100
            print("\nStatistics:\n")
            print(f"  Packets sent: {pings}")
            print(f"  Packets received: {pings - lost_packets}")
            print(f"  Packets lost: {lost_packets} ({loss_rate:.2f}% loss)")
            print(f"  Minimum RTT: {min:.6f} seconds")
            print(f"  Maximum RTT: {max:.6f} seconds")
            print(f"  Average RTT: {avg:.6f} seconds")
        else:
            print("\nNo response received as all packets got lost\n")

        exit = "yes"

        if exit.lower() == 'yes':
            break
        else:
            pings = int(input("Number of pings to send: "))

except Exception as e:
    print(f"Error {e}")

finally:
    client.close()
    print("Connection closed")



