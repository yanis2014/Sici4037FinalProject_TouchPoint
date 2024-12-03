from network import create_socket, send_data
from screen_sharing import capture_screen

def start_server(ip, port):
    server_socket = create_socket(ip, port, is_server=True)
    print(f"Server started at {ip}:{port}")
    conn, addr = server_socket.accept()
    try:
        print(f"Connection established with {addr}")
        while True:
            compressed_data = capture_screen()
            send_data(conn, compressed_data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        server_socket.close()