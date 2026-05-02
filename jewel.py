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


if __name__ == "__main__":
    main()
