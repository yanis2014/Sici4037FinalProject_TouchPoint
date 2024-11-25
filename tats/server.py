import socket
import pickle
import pyautogui
import cv2
import numpy as np

def capture_screen():
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

def apply_input(data):
    input_type, details = data
    if input_type == "mouse_move":
        pyautogui.moveTo(details["x"], details["y"])
    elif input_type == "mouse_click":
        pyautogui.click(button=details["button"])
    elif input_type == "key_press":
        pyautogui.press(details["key"])

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'
    port = 9999
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server listening on port", port)

    client_socket, address = server_socket.accept()
    print("Connection from:", address)

    try:
        while True:
            # Send screen data
            frame = capture_screen()
            frame_data = pickle.dumps(frame)
            client_socket.sendall(len(frame_data).to_bytes(4, 'big') + frame_data)
            
            # Receive input data
            input_len = int.from_bytes(client_socket.recv(4), 'big')
            input_data = client_socket.recv(input_len)
            input_event = pickle.loads(input_data)
            apply_input(input_event)
    except Exception as e:
        print("Error:", e)
    finally:
        client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    main()