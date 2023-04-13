import socket

# create a socket object
client_socket = socket.socket()

# get local machine name
host = 'localhost'
print(host)
# connect to the server on the specified port
client_socket.connect((host, 8080))

data = client_socket.recv(1024)
print('Received data: ' + data.decode())

# receive data from the server
while 1:
    message = input('\nMessage to send: ')
    client_socket.send(message.encode())
    if message == "fim" : break

    print(client_socket.recv(1024).decode())

# close the socket
client_socket.close()
