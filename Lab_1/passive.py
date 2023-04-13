import socket

# create a socket object
server_socket = socket.socket()

# get local machine name
host = ''

# bind the socket to a public host, and a port
server_socket.bind((host, 8080))

# set the server to listen for incoming connections
server_socket.listen(2)

# wait for a connection to be made
print('Waiting for a connection...')
client_socket, address = server_socket.accept()
print('Connection established with ' + str(address))
client_socket.send("Hello client, I'm the echo server".encode())

# receive data from the client
while 1:
    data = client_socket.recv(1024)
    message = data.decode()
    print('Received data: ' + message + "")

    if message == "fim" : break

    client_socket.send("\nServer registered the following message:\n".encode() + message.encode())

# close the socket
client_socket.close()
