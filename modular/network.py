import socket

def create_socket(host, port, is_server=False, max_clients=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if is_server:
        sock.bind((host, port))
        sock.listen(max_clients)
        return sock
    else:
        sock.connect((host, port))
        return sock

def send_data(sock, data):
    data_length = len(data)
    sock.sendall(data_length.to_bytes(4, 'big'))
    sock.sendall(data)

def receive_data(sock):
    data_length_bytes = sock.recv(4)
    if not data_length_bytes:
        return None
    data_length = int.from_bytes(data_length_bytes, 'big')

    data = b""
    while len(data) < data_length:
        packet = sock.recv(min(4096, data_length - len(data)))
        if not packet:
            raise ConnectionError("Incomplete data received")
        data += packet
    return data