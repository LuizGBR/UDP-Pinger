from socket import *
import time
import sys

from statistics import mean, stdev

# fixed configurations
server_ip = '127.0.0.1'
server_port = 30000
n_pings = 10
msg = 'Luiz'

def create_packet(index, message, rtt):
    # create a packet following the documention
    id = str(index).rjust(5, '0') # 5 bytes for index
    request_type = '0' # ping request byte
    timestamp = str(int(rtt / 1000000) % 10000) # 4 bytes for timestamp
    msg = message.ljust(30, '\0') # 30 bytes for message

    packet = id + request_type + timestamp + msg 

    return packet

def response_validate(response, packet):
    if len(response) != 40:
        return False


    validations = [
        packet[0:5] == response[0:5],
        response[5:6] == '1', # pong response
        packet[6:10] == response[6:10],
        packet[10:40] == response[10:40]
    ]

	# if at least one element is False, returns False
    return all(validations)

def print_statistics(rtts, packets_sent, packets_received, total_time):
    if packets_received > 1:
        packet_loss = 100 - packets_received/packets_sent*100
        min_rtt = min(rtts)
        max_rtt = max(rtts)
        avg_rtt = mean(rtts)
        stdev_rtt = stdev(rtts)

        print(f'\n--- {server_ip}:{server_port} ping statistics ---')
        print(f'{str(packets_sent)} packets transmitted, {str(packets_received)} received, {packet_loss}% packet loss, time={total_time} ms')
        print(f'rtt min/avg/max/mdev = {min_rtt:.4}/{avg_rtt:.4}/{max_rtt:.4}/{stdev_rtt:.4} ms')
    
    else:
        print(f'\nThere is not enough data to calculate statistics')

    return

def main():
    # create an UDP socket with IPv4 configuration
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(1)

    # variables for statistics
    n_sent = 0
    n_received = 0
    rtts = []
    total_time = time.time_ns()
    
    for index in range(n_pings):
        rtt = time.time_ns()

        packet = create_packet(index, msg, rtt)
        client_socket.sendto(packet.encode('utf-8'), (server_ip, server_port))
        n_sent += 1

        try:
            response = client_socket.recvfrom(2048)[0]
            response = response.decode('utf-8')

            response_id = int(response[0:5])
            packet_id = int(packet[0:5])

            # wait until find the corresponding response
            while response_id != packet_id:
                response = client_socket.recvfrom(1024)[0]
                response_id = int(response[0:5])

            rtt = time.time_ns() - rtt
            rtt = rtt / 1000000

            if not response_validate(response, packet):
                print('Invalid Response')
                continue

            n_received += 1
            rtts.append(rtt)
            
        
        except timeout:
            print('Timed Out')

    total_time = time.time_ns() - total_time
    total_time = total_time / 1000000

    print_statistics(rtts, n_sent, n_received, total_time)

if __name__ == "__main__":
    main()