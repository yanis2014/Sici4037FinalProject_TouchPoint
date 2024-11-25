import cv2
import pickle
import pyautogui
from pynput import mouse, keyboard
import socket

def receive_screen(client_socket):
    data_len = int.from_bytes(client_socket.recv(4), 'big')
    print("Data len: ", data_len)
    data = b''
    while len(data) < data_len:
        packet = client_socket.recv(data_len - len(data))
        if not packet:
            break
        data += packet
    return pickle.loads(data)

def normalize_coordinates(x, y):
    client_screen_width, client_screen_height = pyautogui.size()
    return x / client_screen_width, y / client_screen_height

def send_input(client_socket, input_event):
    data = pickle.dumps(input_event)
    print(f"Data length: {len(data)}")
    client_socket.sendall(len(data).to_bytes(4, 'big') + data)

def on_mouse_move(x, y):
    norm_x, norm_y = normalize_coordinates(x, y)
    input_event = ("mouse_move", {"x": norm_x, "y": norm_y})
    send_input(client_socket, input_event)

def on_click(x, y, button, pressed):
    if pressed:
        input_event = ("mouse_click", {"x": x, "y": y, "button": button.name})
        send_input(client_socket, input_event)

def on_key_press(key):
    try:
        input_event = ("key_press", {"key": key.char or key.name})
        send_input(client_socket, input_event)
    except AttributeError:
        pass

def main():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host = '10.0.0.136'
    host = '10.0.0.87'
    port = 9999
    client_socket.connect((host, port))
    print("Connected to server")
    
    cv2.namedWindow("TouchPoint", cv2.WINDOW_NORMAL)

    # Start listeners for mouse and keyboard
    mouse_listener = mouse.Listener(on_move=on_mouse_move, on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_key_press)
    mouse_listener.start()
    keyboard_listener.start()

    try:
        while True:
            print("Frame")
            frame = receive_screen(client_socket)
            if frame is None:
                break

            cv2.resizeWindow("TouchPoint", 1024, 768)

            print("Window")
            cv2.imshow("TouchPoint", frame)
            if cv2.waitKey(0) == ord('q'):  # Quit with 'q'
                break
    except Exception as e:
        print("Error:", e)
    finally:
        mouse_listener.stop()
        keyboard_listener.stop()
        client_socket.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()