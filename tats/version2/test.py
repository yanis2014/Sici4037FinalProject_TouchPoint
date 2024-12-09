import tkinter as tk

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
root.mainloop()