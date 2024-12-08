import cv2
import numpy as np
import socket
from PIL import Image
import zlib

def recv_screen(cs):
    # Receive the length of the compressed data first (4 bytes for the size)
    data_length_bytes = cs.recv(4)
    if not data_length_bytes:
        return None  # No data received, return None to handle it gracefully

    # Convert bytes to an integer (big-endian)
    data_length = int.from_bytes(data_length_bytes, 'big')

    # Initialize buffer for receiving data
    compressed_data = b""

    # Receive the complete data based on its length
    while len(compressed_data) < data_length:
        packet = cs.recv(min(4096, data_length - len(compressed_data)))
        if not packet:
            raise ValueError("Connection lost or incomplete data received")
        compressed_data += packet

    # Decompress the received data
    try:
        img_data = zlib.decompress(compressed_data)
    except zlib.error as e:
        raise ValueError(f"Decompression failed: {e}")

    # Convert to an image
    try:
        image = Image.frombytes('RGB', (1200, 675), img_data)
        opencv_image = np.array(image)
        return cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)
    except Exception as e:
        raise ValueError(f"Image reconstruction failed: {e}")


def client_program(host='10.0.43.106', port=9999):
    # Create a TCP/IP Socket
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        cs.connect((host, port))

        while True:
            try:
                opencv_image = recv_screen(cs)
                if opencv_image is None:
                    print("No image received. Closing connection.")
                    break

                # Display the received screen
                cv2.imshow("Client Screen", opencv_image)

                # cv2.setMouseCallback("Client Screen", click_event)
            
                # Exit if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break


            except Exception as e:
                print(f"Error receiving or processing image: {e}")
                break

    finally:
        # Close the client socket and clean up
        cs.close()
        cv2.destroyAllWindows()

""" def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Mouse clicked at: ({x}, {y})")
        cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
        cv2.imshow("Image", img) """