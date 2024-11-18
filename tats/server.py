import socket
import pyautogui
import pickle
import struct

def start_server(host='0.0.0.0', port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} has been established")

    try:
        while True:
            # Capture the screen
            screenshot = pyautogui.screenshot()
            screen_data = screenshot.tobytes()

            # Serialize the screen data
            serialized_data = pickle.dumps(screen_data)
            message_size = struct.pack("L", len(serialized_data))

            # Send the data
            client_socket.sendall(message_size + serialized_data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_server()