# get the URL from the user
import socket

# get the URL from the user
url = input('Enter URL: ')

# split the URL into its component parts
try:
    protocol, _, host, path = url.split('/', 3)
except ValueError:
    print('Invalid URL')
    quit()

# hostname for the socket connect call
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    mysock.connect((host, 80))
except socket.error:
    print('Invalid URL')
    quit()

# send the HTTP GET request
cmd = f'GET /{path} HTTP/1.0\r\nHost: {host}\r\n\r\n'.encode()
mysock.send(cmd)

# count the web page characters received and display them
count = 0
while count <= 1800:
    data = mysock.recv(512)
    if len(data) < 1:
        break
    count += len(data)
    print(data.decode(), end='')

# close the socket connection
mysock.close()
