import socket

# create a socket object
client_socket = socket.socket()

# get local machine name
host = 'localhost'
print(host)
# connect to the server on the specified port
client_socket.connect((host, 5000))

# receive data from the server
while 1:
    message = input('\nMessage to send: ')
    if message == "fim" : break

    client_socket.send(message.encode())

    print(client_socket.recv(1024).decode())

# close the socket
client_socket.close()