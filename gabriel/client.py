# python3 -m pip install package_name

import socket
import pyautogui
import zlib
def client_program():
    host = '10.0.0.136'  # Replace with server's IP address
    port = 65432
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server")
    try:
        while True:
            # Capture the screen
            screenshot = pyautogui.screenshot()
            screenshot = screenshot.resize((800, 600))  # Resize for faster transfer
            # Convert screenshot to bytes
            img_data = screenshot.tobytes()
            # Compress the image data
            compressed_data = zlib.compress(img_data)
            # Send the length of the compressed data followed by the data itself
            data_length = len(compressed_data)
            client_socket.sendall(data_length.to_bytes(4, 'big'))  # Send length first
            client_socket.sendall(compressed_data)
    except Exception as e:
        print("Connection closed or error:", e)
    finally:
        client_socket.close()
if __name__ == "__main__":
    client_program()