""" import tkinter as tk

# Dictionary to track which keys are currently pressed
keys_held = {}

# Function to handle key press
def key_pressed(event):
    if event.keysym not in keys_held:  # Avoid duplicate entries
        keys_held[event.keysym] = True
        print(f"Key Held: {event.keysym}")

# Function to handle key release
def key_released(event):
    if event.keysym in keys_held:
        del keys_held[event.keysym]
        print(f"Key Released: {event.keysym}")

# Create the main application window
root = tk.Tk()
root.title("Key Hold Detector")

# Bind key press and key release events
root.bind("<KeyPress>", key_pressed)
root.bind("<KeyRelease>", key_released)

# Add a label for instructions
label = tk.Label(root, text="Hold any key and check the console.", font=("Arial", 14))
label.pack(pady=20)

# Run the Tkinter event loop
root.mainloop() """

""" import pyautogui

# Hold Shift and type lowercase letters
pyautogui.keyDown("shift")  # Press and hold the Shift key
pyautogui.write("hello world")  # This will type "HELLO WORLD"
pyautogui.keyUp("shift")  # Release the Shift keyHELLO WORLD """

# import tkinter as tk
# import time

# # Initialize variables to track press time and holding state
# press_time = None

# def on_button_press(event):
#     global press_time
#     press_time = time.time()  # Record the time of the press
#     print(f"Mouse button pressed at {event.x}, {event.y}")

# def on_button_release(event):
#     global press_time
#     if press_time is not None:
#         hold_duration = time.time() - press_time  # Calculate duration
#         print(f"Mouse button released at {event.x}, {event.y}")
#         print(f"Hold duration: {hold_duration:.2f} seconds")
#         press_time = None  # Reset the press time

# # Create the main application window
# root = tk.Tk()
# root.title("Mouse Hold Detector")

# # Bind mouse events
# root.bind("<ButtonPress-1>", on_button_press)  # Left mouse button
# root.bind("<ButtonRelease-1>", on_button_release)  # Left mouse button release

# # Add a label to provide instructions
# label = tk.Label(root, text="Press and hold the left mouse button anywhere.", font=("Arial", 14))
# label.pack(pady=20)

# # Run the Tkinter event loop
# root.mainloop()

import tkinter as tk

def on_scroll(event):
    print(event.delta)

root = tk.Tk()
root.title("Mouse Scroll Example")
root.geometry("300x200")

# Bind mouse wheel event
root.bind("<MouseWheel>", on_scroll)  # Windows and MacOS
# root.bind("<Button-4>", lambda event: print("Scrolled up"))  # Linux (scroll up)
# root.bind("<Button-5>", lambda event: print("Scrolled down"))  # Linux (scroll down)

root.mainloop()