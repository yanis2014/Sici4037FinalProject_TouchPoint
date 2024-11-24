# python3 -m pip install package_name
import socket
import cv2
import numpy as np
import zlib
from PIL import Image
def client_program(host='10.0.0.136', port=65432):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server")

    try:
        while True:
            # Receive the length of the compressed data first
            data_length = int.from_bytes(client_socket.recv(4), 'big')
            compressed_data = b""
            # Receive the compressed data in chunks
            while len(compressed_data) < data_length:
                packet = client_socket.recv(4096)
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
        client_socket.close()
        cv2.destroyAllWindows()
if __name__ == "__main__":
    client_program()