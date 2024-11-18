import socket

# Client Code
def start_client(server_ip, port=9999, message="Hello, Server!"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, port))
        client_socket.sendall(message.encode('utf-8'))
        print("Message sent to the server.")


if __name__ == "__main__":
    # To run the server, uncomment the line below and run the script on the server machine
    # start_server()

    # To run the client, uncomment the line below and run the script on the client machine
    # Replace 'server_ip' with the IP address of the server machine
    start_client('10.0.43.89')