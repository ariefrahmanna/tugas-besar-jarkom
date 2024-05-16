import socket


# IP_ADDRESS = '10.60.14.12'
IP_ADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 80

# setup server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP_ADDRESS, PORT))
server.listen(5)
print("Server siap untuk menerima request...")

while True:
    # menerima request masuk dari client
    client, addr = server.accept()
    client_ip = addr[0]
    print("Request koneksi dari:", client_ip)

    # memproses request dari client
    request = client.recv(1024).decode()
    path = request.split()[1]
    file_name = path[1:] if path != '/' else 'index.html'

    try:
        # mencari konten sesuai request dari client
        with open(file_name) as f:
            content = f.read()

        # kirim response konten
        response = f"HTTP/1.1 200 OK\r\n\r\n{content}\r\n"
        client.send(response.encode())
        print(f'file {file_name} terkirim pada {client_ip}')

    except IOError:
        # kirim response file not found
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
        client.send(response.encode())
        print(f'file not found terkirim pada {client_ip}')

    # tutup koneksi client
    client.close()
