import tkinter as tk
import socket

import server
import client

from threading import Timer

# Check if entry is a valid IP
def is_valid_ip(ip):
    try:
        splt = ip.split(".")
        for i in range(len(splt)):
            elem = int(splt[i])
            if not (0 <= elem <= 255):
                return False
        return len(splt) == 4
    except:
        return False

# Check if entry is a valid port
def is_valid_port(port):
    try:
        elem = int(port)
        return (0 <= elem <= 65535)
    except:
        return False

# Clears the error labels
def clear_err_labels():
    op1_ip_err_label.configure(text="")
    op1_port_err_label.configure(text="")
    op2_port_err_label.configure(text="")

# Clears the entries
def clear_entries():
    op1_ip_entry.delete(0,tk.END)
    op1_port_entry.delete(0,tk.END)
    op2_port_entry.delete(0,tk.END)

# Function to enable/disable input fields based on selected radio button
def toggle_inputs():
    clear_err_labels()
    if selected_option.get() == "Option 1":
        state1 = "normal"
        state2 = "disabled"
    else: 
        state1 = "disabled"
        state2 = "normal"
    op1_ip_entry.configure(state=state1)
    op1_port_entry.configure(state=state1)
    op2_port_entry.configure(state=state2)
    op1_ip_label.configure(state=state1)
    op1_port_label.configure(state=state1)
    op2_port_label.configure(state=state2)

# Returns true if invalid entry is found
def validate_entries(op1_ip, op1_port, op2_port):
    # Initialize invalid entry flag
    invalid_entry = False

    # Validates the ip entry if option 1 is enabled
    if op1_ip_entry.cget("state") == "normal" and not is_valid_ip(op1_ip):
        op1_ip_err_label.configure(text=f" * Invalid IP Address: '{op1_ip}'")
        op1_ip_entry.delete(0, tk.END)
        invalid_entry = True
    
    # Validates the ip entry if option 1 is enabled
    if op1_port_entry.cget("state") == "normal" and not is_valid_port(op1_port):
        op1_port_err_label.configure(text=f" * Invalid Port: '{op1_port}'")
        op1_port_entry.delete(0, tk.END)
        invalid_entry = True
    
    # Validates the ip entry if option 1 is enabled
    if op2_port_entry.cget("state") == "normal" and not is_valid_port(op2_port):
        op2_port_err_label.configure(text=f" * Invalid Port: '{op2_port}'")
        op2_port_entry.delete(0, tk.END)
        invalid_entry = True

    return invalid_entry


# Triggers connection based on selected option
def click_connect():
    # Clear errors labels
    clear_err_labels()

    # Get connection details
    op1_ip = op1_ip_entry.get()
    op1_port = op1_port_entry.get()
    op2_port = op2_port_entry.get()

    # Terminate if invalid entry
    if validate_entries(op1_ip, op1_port, op2_port):
        return

    # Client option selected
    if selected_option.get() == "Option 1":
        
        # Close the gui window
        window.destroy()

        # Run client program
        client.client_program(hostserver=op1_ip, port=int(op1_port))
    
    # Server option selected
    else:
        # Open listening window
        server_connect_window(op2_port)

        # Refresh window
        window.update_idletasks()
        window.update()

        # Run server program
        server.server_program(port=int(op2_port), window=window)

def server_connect_window(port):
    # Clear the current frame
    for widget in main_frame.winfo_children():
        widget.pack_forget()

    # Edit status text
    server_connect_status.configure(text=f"{socket.gethostbyname(socket.gethostname())} is listening on port {port}...")
    
    # Place widgets
    server_connect_header.pack(anchor="w", padx=10, pady=30)
    server_connect_status.pack(anchor="w", padx=10)
    cancel_button.pack(anchor="w", padx=10, pady=35)

def main_window():
    # Clear the current frame
    for widget in main_frame.winfo_children():
        widget.pack_forget()

    # Clear entries
    clear_entries()

    # Put input and error labels next to each other
    op1_ip_entry.grid(row=0, column=0)
    op1_ip_err_label.grid(row=0, column=1, padx= 10)

    op1_port_entry.grid(row=0, column=0)
    op1_port_err_label.grid(row=0, column=1, padx= 10)

    op2_port_entry.grid(row=0, column=0)
    op2_port_err_label.grid(row=0, column=1, padx= 10)

    # Place main window widgets
    instruction_label.pack(anchor="w", pady=10, padx=10)

    radio_buttons["Option 1"].pack(anchor="w", pady=10, padx=10)
    op1_ip_label.pack(anchor="w", padx=35)
    op1_ip_frame.pack(anchor="w", padx=35)
    op1_port_label.pack(anchor="w", padx=35)
    op1_port_frame.pack(anchor="w", padx=35)

    radio_buttons["Option 2"].pack(anchor="w", pady=10, padx=10)
    op2_port_label.pack(anchor="w", padx=35)
    op2_port_frame.pack(anchor="w", padx=35)

    connect_button.pack(anchor="w", pady=20, padx=20)

    toggle_inputs()  # Reset the inputs based on the current selection

if __name__ == "__main__":
    
    # Create the main window
    window = tk.Tk()

    # Set the window title
    window.title("TouchPoint - Remote Desktop Connection")

    # Set window size and position
    window.resizable(True,True)

    # Create a frame for the main window
    main_frame = tk.Frame(window)
    main_frame.pack(fill="both", expand=True)

    # Create instruction label
    instruction_label = tk.Label(
        main_frame, 
        text="Please choose an option below and enter the corresponding information:")

    # Stores the selected option
    selected_option = tk.StringVar(value="Option 1")

    # Create two radio buttons
    radio_buttons = {}
    radio_buttons["Option 1"] = tk.Radiobutton(
        main_frame, 
        text="Connect to Another Computer", 
        value="Option 1", 
        variable=selected_option, 
        command=toggle_inputs)
    radio_buttons["Option 2"]= tk.Radiobutton(
        main_frame, 
        text="Allow Connection to Your Computer", 
        value="Option 2", 
        variable=selected_option, 
        command=toggle_inputs)

    # Create labels
    op1_ip_label = tk.Label(main_frame, text="IP Address:")
    op1_port_label = tk.Label(main_frame, text="Port:")
    op2_port_label = tk.Label(main_frame, text="Port:")

    # Create frames for input and error labels
    op1_ip_frame = tk.Frame(main_frame)
    op1_port_frame = tk.Frame(main_frame)
    op2_port_frame = tk.Frame(main_frame)

    # Create entry boxes
    op1_ip_entry = tk.Entry(op1_ip_frame)
    op1_port_entry = tk.Entry(op1_port_frame)
    op2_port_entry = tk.Entry(op2_port_frame)

    # Create error labels
    op1_port_err_label = tk.Label(op1_port_frame, text="", fg="red")
    op1_ip_err_label = tk.Label(op1_ip_frame, text="", fg="red")
    op2_port_err_label = tk.Label(op2_port_frame, text="", fg="red")

    # Create Connect button
    connect_button = tk.Button(
        main_frame, 
        text="Connect", 
        bg="blue", 
        fg="white", 
        command=click_connect
    )

    # Create server connection header label
    server_connect_header = tk.Label(
        main_frame, 
        text=radio_buttons["Option 2"].cget("text"), 
        font = ('Calibri', 16))

    # Create server connection status label
    server_connect_status = tk.Label(main_frame)

    # Create cancel button
    cancel_button = tk.Button(
        main_frame, 
        text="Cancel", 
        bg="red", 
        fg="white" #,
        #command
    )

    # Initial state of inputs (enabled for Option 1)
    toggle_inputs()

    # Create Connect button
    connect_button = tk.Button(main_frame, text="Connect", bg="blue", fg="white", command=click_connect)

    # Place widgets
    main_window()

    # Runs the application
    window.mainloop()