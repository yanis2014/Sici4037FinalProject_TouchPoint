import socket
import pickle
import struct
import cv2
import numpy as np

def start_client(server_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    data = b""
    payload_size = struct.calcsize("L")

    try:
        while True:
            # Retrieve message size
            while len(data) < payload_size:
                packet = client_socket.recv(4096)
                if not packet:
                    break
                data += packet
            print("Data packet received")
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]

            # Retrieve all data based on message size
            while len(data) < msg_size:
                data += client_socket.recv(4096)

            serialized_data = data[:msg_size]
            data = data[msg_size:]

            # Deserialize the data and display it
            screen_data = pickle.loads(serialized_data)
            screen_array = np.frombuffer(screen_data, dtype=np.uint8)
            screen = cv2.imdecode(screen_array, cv2.IMREAD_COLOR)

            # Show the screen using OpenCV
            cv2.imshow("Remote Desktop", screen)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    start_client("10.0.43.89", 9999)