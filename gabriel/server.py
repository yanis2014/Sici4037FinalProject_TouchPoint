import socket
import pyautogui
import zlib
def server_program(host='0.0.0.0', port=65432):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server is waiting for a connection...")
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

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
            conn.sendall(data_length.to_bytes(4, 'big'))  # Send length first
            conn.sendall(compressed_data)
    except Exception as e:
        print("Connection closed or error:", e)
    finally:
        server_socket.close()
        
if __name__ == "__main__":
    server_program()