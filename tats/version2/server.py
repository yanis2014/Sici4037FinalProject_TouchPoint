import socket
import pyautogui
import zlib

from threading import Thread, Event
import time
import sys


# CONFIG
x_max = 1200    # pixels in x-axis
y_max = 675     # pixels in y-axis

# establish connection
def connect(sock):
    while 1:
        try:
            sock.settimeout(3)     # configure max wait time on blocking calls (seconds)
            conn, addr = sock.accept()
            sock.settimeout(None)  # reset timeout to None
            return conn, addr
        except TimeoutError: # allows the KeyboardInterrupt to be raised while establishing conn
            pass # do nothing, i.e. reattempt connection (while loop)


# Send one screenshot to the client
def send_screen(client):
    # Capture the screen
    screenshot = pyautogui.screenshot()
    screenshot = screenshot.resize((x_max, y_max))

    # Convert screenshot to bytes
    screen_data = screenshot.tobytes()

    # Compress the image data
    compressed_data = zlib.compress(screen_data)

    # Send the length of the compressed data
    data_length = len(compressed_data)
    client.sendall(data_length.to_bytes(4,'big'))
    client.sendall(compressed_data)

# Process one input from the client
def read_input(client):
    inp = client.recv(1024)     # read from the socket
    inp = inp.decode('utf-8')   # decode the string
    print(inp)
    
    # parse message
    inp = inp.split(" ")
    x_rel = float(inp[0].split(":")[1]) # relative x coordinate
    y_rel = float(inp[1].split(":")[1]) # relative y coordinate
    event = float(inp[0].split(":")[1]) # event type

    # convert coordinates
    x_abs, y_abs = abs_coord(x_rel, y_rel)
    pyautogui.moveTo(x_abs, y_abs)
    pyautogui.click(x_abs, y_abs, button="left")

# return absolute coordinates from relative
def abs_coord(x_percent, y_percent):
    x_max, y_max = pyautogui.size()
    return int(x_percent*x_max), int(y_percent*y_max)

# return relative coodinates from absolute, using decimals from 0 to 1
def rel_coord(x_abs, y_abs):
    x_max, y_max = pyautogui.size()
    return x_abs/x_max, y_abs/y_max

# ---- THREAD LOOPS ---- #
# process all input from client
def input_receiver(conn, done):
    while not done.is_set():
        read_input(conn)
    sys.exit(0) # terminate this thread explicitly

# continuously send client video
def video_sender(conn, done):
    while not done.is_set():
        send_screen(conn)
    sys.exit(0) # terminate this thread explicitly
# ---------------------- #

# Runs the server program
def server_program(port=9999):

    hostname = socket.gethostname()     # get this machine's name
    hostaddr = socket.gethostbyname(hostname)   # get this machine's address

    host = hostaddr

    # Creates a TCP/IP socket
    video_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ui_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    done = Event()  # stopping condition for threads
    done.clear()    # clear to false

    # Bind the to the address and port
    video_sock.bind((host, port))
    ui_sock.bind((host, port + 1))

    # Enable the server to accept connection (max 1 queued connections)
    video_sock.listen(1)
    ui_sock.listen(1)

    # Notify server has started
    print(f"Video Server started at {host} Port: {port}.")
    print(f"UI Server started at {host} Port: {port + 1}.")

    try:
        print("Awaiting connections...")
        
        video_conn, video_addr = connect(video_sock)    # outbound video feed
        print(f"Video connection to {video_addr} has been established.")
        
        ui_conn, ui_addr = connect(ui_sock)             # inbound user input
        print(f"Input connection from {ui_addr} has been established.")
        
        # create threads
        video_thread = Thread(target=video_sender, args=(video_conn, done), daemon=True)
        input_thread = Thread(target=input_receiver, args=(ui_conn, done), daemon=True)

        # launch threads
        video_thread.start()
        input_thread.start()

        # wait until keyboard interrupt stops the loop
        while not done.is_set():
            time.sleep(100)

    except KeyboardInterrupt:
        print("Server is shutting down.")
        done.set()

    finally:
        done.set()  # tell threads to stop

        # wait until threads stop
        video_thread.join()
        input_thread.join()

        # close sockets    
        video_sock.close()
        ui_sock.close()

        # terminate main program
        sys.exit(0)

if __name__ == "__main__":
    server_program()