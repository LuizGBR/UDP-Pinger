from socket import *
import random
import time

# fixed configurations
recieve_host = '127.0.0.1'
recieve_port = 30000

# create a UDP socket
server_socket = socket(AF_INET, SOCK_DGRAM)
# assign IP address and port number to socket
server_socket.bind((recieve_host, recieve_port))


# control settings:
simulate_delay = True
simulate_protocol_error = True

while True:
  try:
    message, address = server_socket.recvfrom(2048)

    message = message.decode('utf-8')

    message_id = message[0:5]
    message_control_byte = message[5:6]
    message_timestamp = message[6:10]
    message_content = message[10:40]


  
    if message_control_byte == '0':
      message_control_byte = '1' # pong response byte
    else:  # packet error
      server_socket.sendto(message.encode('utf-8'), address)
      print('ERROR: ping/pong error.')
      continue
  
    # protocol error
    if simulate_protocol_error:
      if random.random() < 0.2:
          pass
      elif random.random() < 0.2:
          message_control_byte = '13'
          print('Simulating Ping/Pong error')
      elif random.random() < 0.2:
          message_timestamp = '0000'
          print('Simulating Timestamp error')


    # sending message
    response = message_id + message_control_byte + message_timestamp + message_content    

    # with delay
    if simulate_delay:
      server_socket.sendto(response.encode('utf-8'), address)
      print(f'Message sent: {message} ')
      time.sleep(0.2)
    else: #without delay
      server_socket.sendto(response.encode('utf-8'), address)
      print(f'Message sent: {message} ')

  except error:
    print(f'Error {error}')