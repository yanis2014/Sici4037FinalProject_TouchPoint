import socket
import pickle
import cv2
from pynput import mouse, keyboard

def receive_screen(client_socket):
    data_len = int.from_bytes(client_socket.recv(4), 'big')
    data = b''
    while len(data) < data_len:
        packet = client_socket.recv(data_len - len(data))
        if not packet:
            break
        data += packet
    return pickle.loads(data)

def send_input(client_socket, input_event):
    data = pickle.dumps(input_event)
    client_socket.sendall(len(data).to_bytes(4, 'big') + data)

def on_mouse_move(x, y):
    input_event = ("mouse_move", {"x": x, "y": y})
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
    host = 'server_ip_address'
    port = 9999
    client_socket.connect((host, port))
    print("Connected to server")

    # Start listeners for mouse and keyboard
    mouse_listener = mouse.Listener(on_move=on_mouse_move, on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_key_press)
    mouse_listener.start()
    keyboard_listener.start()

    try:
        while True:
            frame = receive_screen(client_socket)
            cv2.imshow("Remote Desktop", frame)
            if cv2.waitKey(1) == ord('q'):  # Quit with 'q'
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