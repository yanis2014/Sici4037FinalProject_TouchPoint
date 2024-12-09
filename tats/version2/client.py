import tkinter as tk
import socket
from PIL import Image, ImageTk
import zlib

from threading import RLock

# CONFIG
x_max = 1200    # pixels in x-axis
y_max = 675     # pixels in y-axis


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
        image = Image.frombytes('RGB', (x_max, y_max), img_data)
        return ImageTk.PhotoImage(image)
    
    except Exception as e:
        raise ValueError(f"Image reconstruction failed: {e}")

SOCK_LOCK = RLock()

def send(msg):
    msg += " "
    with SOCK_LOCK:
        print(msg)
        payload = msg.encode('utf-8')
        ui_sock.sendall(payload)

# ----- KEYBOARD FUNCTIONS ----- #

# Dictionary to track which keys are currently pressed
keys_held = {}

# Function to handle key press
def key_pressed(event):
    print("key pressed")
    if event.keysym not in keys_held:  # Avoid duplicate entries
        keys_held[event.keysym] = True
        msg = f"KD {event.keysym}"
        send(msg)

# Function to handle key release
def key_released(event):
    print("key released")
    if event.keysym in keys_held:
        del keys_held[event.keysym]
        msg = f"KU {event.keysym}"
        send(msg)

# ------ MOUSE FUNCTIONS ------ #

# def left_click_handler(event):
#     x_rel = event.x/x_max
#     y_rel = event.y/y_max
#     msg = f"MDL {x_rel} {y_rel}"
#     send(msg)

def mouse_press(event):
    x_rel = event.x/x_max
    y_rel = event.y/y_max
    command = "MD"

    if event.num == 1:
        command += "L"
    elif event.num == 3:
        command += "R"
    else:
        return 0

    msg = f"{command} {x_rel} {y_rel}"
    send(msg)

def mouse_release(event):
    x_rel = event.x/x_max
    y_rel = event.y/y_max
    command = "MU"

    if event.num == 1:
        command += "L"
    elif event.num == 3:
        command += "R"
    else:
        return 0

    msg = f"{command} {x_rel} {y_rel}"
    send(msg)




    

# return absolute coordinates from relative
def abs_coord(x_percent, y_percent):
    return int(x_percent*x_max), int(y_percent*y_max)

# return relative coodinates from absolute, using decimals from 0 to 1
def rel_coord(x_abs, y_abs):
    return x_abs/x_max, y_abs/y_max


# ----- MAIN ----- #

def client_program(hostserver=None, port=9999):

    hostname = socket.gethostname()     # get this machine's name
    hostaddr = socket.gethostbyname(hostname)   # get this machine's address

    print(f"Client started at {hostaddr}")

    # Create a TCP/IP Sockets
    global video_sock
    global ui_sock
    video_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ui_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    video_server = (hostserver, port)
    ui_server = (hostserver, port + 1)

    try:
        # Connect to the server video feed
        print(f"Connecting to server video feed at {video_server}...")
        video_sock.connect(video_server)    # recieves images
        print("Video feed established.")

        print(f"Connecting to server user input at {ui_server}...")
        ui_sock.connect(ui_server)   # sends user input
        print("User input established.")

        # create tk window
        window = tk.Tk()
        window.title("Reciever")
        window.geometry("500x300")

        # create widget to display feed
        label = tk.Label(window)
        label.pack()

        # bind mouseclicks to image
        label.bind("<ButtonPress>", mouse_press)
        label.bind("<ButtonRelease>", mouse_release)

        # Bind key press and key release events
        window.bind("<KeyPress>", key_pressed)
        window.bind("<KeyRelease>", key_released)

        while True:
            try:
                tk_image = recv_screen(video_sock)
                if tk_image is None:
                    print("No image received. Closing connection.")
                    break

                # Display the received screen
                label.configure(image=tk_image)

                window.update_idletasks()
                window.update()

        
            except Exception as e:
                print(f"Error receiving or processing image: {e}")
                break

    finally:
        # Close the client socket and clean up
        video_sock.close()
        ui_sock.close()


if __name__ == "__main__":
    hostaddr = input("Enter server: ")
    client_program(hostserver=hostaddr)
    # client_program(hostserver='10.0.0.87')

""" def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Mouse clicked at: ({x}, {y})")
        cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
        cv2.imshow("Image", img) """