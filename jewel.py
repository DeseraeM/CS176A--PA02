#!/usr/bin/env python3

# What Needs to Be Built:
#   1. HTTP request parser   — split on \r\n\r\n, parse method/path/headers
#   2. select.select() loop  — track the listening socket + all open client
#                              sockets; buffer partial reads per connection;
#                              keep connections open after responding (keep-alive)
#   3. HTTP response builder — status line, Content-Type, Content-Length, body
#   4. Full error handling   — 400, 404, 501
#
# FileReader (file_reader.py):
#   5. get()  — returns file bytes, or an HTML directory listing, or None
#   6. head() — returns byte count, or None

import socket
import sys

from file_reader import FileReader


def main():
    port = int(sys.argv[1])
    file_path = sys.argv[2]

    file_reader = FileReader(file_path)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allows reuse of port immediately after server restart
    s.bind(("0.0.0.0", port))
    s.listen(50)

    while True:
        (client, address) = s.accept()
        data = client.recv(1024)
        print(data)
        readable, writable, exceptional = select.select(info, output, info)


if __name__ == "__main__":
    main()

#1. HTTP request parse
#\r\n\r\n means the end of a header and the \r\n is used for all the other lines 
incoming = (
    #OR "File_path/File"
    "GET /Mymethod/file_path HTTP/1.1\r\n"
    "Host: address\r\n"
    "Port: connection\r\n"
    "User: client\r\n"
    "MyHeader: MyValue\r\n\r\n" 
)
header_e = incoming.find('\r\n\r\n')
 if header_e <= -1:
        return "400"

elif if header_e > -1:
    header = incoming[:header_e]
    lines = header.split('\r\n')
    request = lines[0].split()
    if not request[1]:
        return "404"
    if request[0] != 'GET':
        return "501 Method Unimplemented"
    headerL = lines[1:]
    print(request)
    for h in headerL:
        new_header = h.split(':')
        key = new_header[0].strip()
        val = new_header[1].strip()
        print('{}: {}'.format(key,val))

#select.select() loop
info = [s]
output = []
messages = {}
readable, writable, exceptional = select.select(info, output, info)
for sock in readable:
    if sock is s:
        connection, address = s.accept()
        print('new connection from', address, connection)
        info.append(connection)
        messages[connection]= ""
    else:
        data = sock.recv(1024)
        if data:
            messages[sock] += data
            if sock not in output:
                output.append(sock)
        else:
            info.remove(sock)
            messages.pop(sock,"")
            sock.close()


for sock in exceptional:
    info.remove(sock)
    if sock in output:
         output.remove(sock)
        sock.close()
        messages.pop(sock,"")

#3. HTTP response builder 
incoming = (
    "HTTP/1.1 200 OK\r\n"
    "Connection: close\r\n"
    "User: client\r\n"
    "Server: server\r\n" 
    "Last-Modified: Modified\r\n"
    "Content-Length: Length\r\n" 
    "Content-Type: Type\r\n\r\n" 
)
response_H = incoming.find('\r\n\r\n')
if response_H <= -1:
    return "400"
else:
    header_R = incoming[:response_H]
    lines = header_R.split('\r\n')
    requestR = lines[0].split()
    r = lines[1:]
    print(requestR)
    for respond in r:
        new_r = respond.split(':')
        key = new_r[0].strip()
        val = new_r[1].strip()
        print('{}: {}'.format(key,val))
#Full error handling -- have a true or false and then return the number assoicated with it.
    if respond_H <= -1:
        return "400"
    if not request[1]:
        return "404"
    if request[0] != 'GET':
        return "501 Method Unimplemented"