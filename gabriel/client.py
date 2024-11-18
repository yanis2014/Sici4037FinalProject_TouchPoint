import socket
import pyautogui
import zlib
import cv2
import struct
import numpy as np

def client_program(server_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server")

    data = b""
    payload_size = struct.calcsize("L")

    try:
        while True:
            # Receive the length of the compressed data first
            data_length = int.from_bytes(conn.recv(4), 'big')
            compressed_data = b""

            # Receive the compressed data in chunks
            while len(compressed_data) < data_length:
                packet = conn.recv(4096)
                if not packet:
                    break
                compressed_data += packet

            # Decompress the received data
            img_data = zlib.decompress(compressed_data)
            image = Image.frombytes('RGB', (800, 600), img_data)
            opencv_image = np.array(image)
            opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)

            # Display the screen image
            cv2.imshow("Client Screen", opencv_image)
            if cv2.waitKey(1) == ord("q"):
                break
    except Exception as e:
        print("Connection closed or error:", e)
    finally:
        conn.close()
        cv2.destroyAllWindows()

"""     try:
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
        client_socket.close() """

if __name__ == "__main__":
    client_program('10.0.43.89', 65432)