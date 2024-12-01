import socket
import pyautogui
import zlib


def send_screen(client):
    # Capture the screen
    screenshot = pyautogui.screenshot()
    screenshot = screenshot.resize((1200, 675))

    # Convert screenshot to bytes
    screen_data = screenshot.tobytes()

    # Compress the image data
    compressed_data = zlib.compress(screen_data)

    # Send the length of the compressed data
    data_length = len(compressed_data)
    client.sendall(data_length.to_bytes(4,'big'))
    client.sendall(compressed_data)



# Runs the server program
def server_program(host='0.0.0.0', port=9999):
    ############### Testing Vars
    data = "x"

    # Creates a TCP/IP socket
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the to the address and port
    ss.bind((host, port))

    # Enable the server to accept connection (max 1 queued connections)
    ss.listen(1)

    # Notify server has started
    print(f"Server started at {host} Port: {port}.")

    try:
        # Wait for a connection
        conn, addr = ss.accept()
        print(f"Connection from {addr} has been established.")

        # Receive data
        while True:
            send_screen(conn)

    except KeyboardInterrupt:
        print("Server is shutting down.")

    finally:
        ss.close()

if __name__ == "__main__":
    server_program()