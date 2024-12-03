from network import create_socket, receive_data
from screen_sharing import decompress_screen
import cv2

def start_client(ip, port):
    client_socket = create_socket(ip, port)
    try:
        while True:
            compressed_data = receive_data(client_socket)
            if compressed_data is None:
                break
            frame = decompress_screen(compressed_data)
            cv2.imshow("Remote Screen", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        client_socket.close()
        cv2.destroyAllWindows()