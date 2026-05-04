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
import select
import os

from file_reader import FileReader

#1. HTTP request parse
#\r\n\r\n means the end of a header and the \r\n is used for all the other lines 
def req(data,file_reader,cookies):
   # incoming = (
    #    "GET /Mymethod/file_path HTTP/1.1\r\n"
     #   "Host: address\r\n"
      #  "Port: connection\r\n"
       # "User: client\r\n"
       # "MyHeader: MyValue\r\n\r\n" 
    #)
    header_e = data.find(b'\r\n\r\n')
    if header_e <= -1:
            return "400"
    else:
        header = data[:header_e]
        lines = header.split(b'\r\n')
        request = lines[0].split()
        if not request[1]:
            return "404"
        if request[0] != b'GET':
            return "501 Method Unimplemented"
        headerL = lines[1:]
        print(request)
        c_cookies = []
        for h in headerL:
            new_header = h.split(':')
            key = new_header[0].strip()
            val = new_header[1].strip()
            if key == "Cookies":
                c_cookies.append(val)
            print('{}: {}'.format(key,val))
        feedback = respondB(request[1], file_reader, c_cookies)
        return feedback
#select.select() loop
def selectS(s,file_reader, cookies): 
    info = [s]
    output = []
    messages = {}
    while True: 
        readable, writable, exceptional = select.select(info, output, info)
        for sock in readable:
            if sock is s:
                connection, address = s.accept()
                print('new connection from', address, connection)
                info.append(connection)
                messages[connection]= b""
            else:
                data = sock.recv(1024)
                if data:
                    messages[sock] += data
                    messageO= req(data,file_reader)
                    if isinstance(messageO,bytes):
                        sock.send(messageO)
                    else:
                        sock.send(messageO.encode('utf-8'))
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
def respondB(file_path,file_reader, cookies):
    #incoming = (
     #   "HTTP/1.1 200 OK\r\n"
      #  "Connection: close\r\n"
       # "User: client\r\n"
       # "Server: server\r\n" 
       # "Last-Modified: Modified\r\n"
        #"Content-Length: Length\r\n" 
        #"Content-Type: Type\r\n\r\n" 
    #)
    status = "HTTP/1.1 200 OK"
    contentL = file_reader.head(file_path, cookies)
    pathType = os.path.splitext(file_path)
    mType = ""
    if pathType[1] == '.html':
        mType = "text/html"
    elif  pathType[1] == '.css':
        mType = "text/ccs"
    elif  pathType[1] == '.png':
        mType = "image/png"
    elif  pathType[1] == '.jpeg':
        mType = "image/jpeg"
    bodyT = file_reader.get(file_path,cookies)
    word = f"{status}\r\nContent-Type: {mType}\r\nContent-Length: {contentL}\r\n\r\n".encode() + bodyT
    return word
#Full error handling -- have a true or false and then return the number assoicated with it.
#def error():
 #  if respond_H <= -1:
  #      return "400"
   # if not request[1]:
    #    return "404"
    #if request[0] != 'GET':
     #   return "501 Method Unimplemented"

def main():
    port = int(sys.argv[1])
    file_path = sys.argv[2]

    file_reader = FileReader(file_path)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allows reuse of port immediately after server restart
    s.bind(("0.0.0.0", port))
    s.listen(50)
    selectS(s,file_reader) 


if __name__ == "__main__":
    main()