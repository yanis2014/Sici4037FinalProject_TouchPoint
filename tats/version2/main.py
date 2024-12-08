import tkinter as tk
import socket

import server
import client

from threading import Timer

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
    
def is_valid_port(port):
    try:
        elem = int(port)
        return (0 <= elem <= 65535)
    except:
        return False
    

def clear_err_labels():
    err_label1.configure(text="")
    err_label2.configure(text="")
    err_label3.configure(text="")

def clear_entries():
    entry1.delete(0,tk.END)
    entry2.delete(0,tk.END)
    entry3.delete(0,tk.END)

# Function to enable/disable input fields based on selected radio button
def toggle_inputs():
    clear_err_labels()
    if selected_option.get() == "Option 1":
        state1 = "normal"
        state2 = "disabled"
    else: 
        state1 = "disabled"
        state2 = "normal"
    entry1.configure(state=state1)
    entry2.configure(state=state1)
    entry3.configure(state=state2)
    label1.configure(state=state1)
    label2.configure(state=state1)
    label3.configure(state=state2)

# Triggers connection based on selected option
def click_connect():
    # Clear errors labels
    clear_err_labels()

    # Initialize invalid entry flag
    invalid_entry = False

    # Get connection details
    op1_ip = entry1.get()
    op1_port = entry2.get()
    op2_ip = socket.gethostbyname(socket.gethostname())
    op2_port = entry3.get()
    
    # Validate entries
    if entry1.cget("state") == "normal" and not is_valid_ip(op1_ip):
        err_label1.configure(text=f" * Invalid IP Address: '{op1_ip}'")
        entry1.delete(0, tk.END)
        invalid_entry = True
    
    if entry2.cget("state") == "normal" and not is_valid_port(op1_port):
        err_label2.configure(text=f" * Invalid Port: '{op1_port}'")
        entry2.delete(0, tk.END)
        invalid_entry = True
    
    if entry3.cget("state") == "normal" and not is_valid_port(op2_port):
        err_label3.configure(text=f" * Invalid Port: '{op2_port}'")
        entry3.delete(0, tk.END)
        invalid_entry = True

    # Terminate if invalid entry
    if invalid_entry:
        invalid_entry = False
        return
    
    window.destroy()

    if selected_option.get() == "Option 1":     # This is client
        client.client_program(hostserver=op1_ip, port=int(op1_port))
    
    else:   # This is a server
        server.server_program(port=int(op2_port))

    # # Clear the previous content (widgets) from the window
    # for widget in main_frame.winfo_children():
    #     widget.pack_forget()

    # # Get the selected option
    # option = selected_option.get()
    # option_text = radio_buttons[option].cget("text")
    
    # # Create a header label at the top of the status window
    # header_label = tk.Label(main_frame, text=option_text, font=("Calibri", 16, "bold"))
    # header_label.pack(anchor="w", pady=10, padx=10)

    
    # # Create status label
    # status_label = tk.Label(main_frame, text="Status: Initializing...")
    # status_label.pack(anchor="w", padx=10, pady=20)

    # def update_status(message):
    #     status_label.configure(text=f"Status: {message}")

    # if option == "Option 1":
    #     update_status(f"Status: Connecting to {op1_ip} on port {op1_port}...")
    #     # main_frame.after(100, lambda: test_client.start_client(op1_ip, int(op1_port), status_callback=update_status))
    # else:
    #     update_status(f"Status: {op2_ip} is listening on port {op2_port}...")
    #     # main_frame.after(100, lambda: test_server.start_server(op2_ip, int(op2_port), status_callback=update_status))
        
    # # Create Cancel button
    # end_button = tk.Button(main_frame, text="Cancel", bg="red", fg="white", command=return_to_main)
    # end_button.pack(anchor="w", pady=20, padx=10)


def return_to_main():
    # Clear the current frame
    for widget in main_frame.winfo_children():
        widget.pack_forget()

    # Clear entries
    clear_entries()

    # Re-add the main window widgets
    instruction_label.pack(anchor="w", pady=10, padx=10)
    radio_buttons["Option 1"].pack(anchor="w", pady=10, padx=10)
    label1.pack(anchor="w", padx=35)
    ip_frame.pack(anchor="w", padx=35)
    label2.pack(anchor="w", padx=35)
    port1_frame.pack(anchor="w", padx=35)
    radio_buttons["Option 2"].pack(anchor="w", pady=10, padx=10)
    label3.pack(anchor="w", padx=35)
    port2_frame.pack(anchor="w", padx=35)
    connect_button.pack(anchor="w", pady=20, padx=20)
    toggle_inputs()  # Reset the inputs based on the current selection

if __name__ == "__main__":
    # Create the main window
    window = tk.Tk()

    # Set the window title
    window.title("TouchPoint - Remote Desktop Connection")

    # Set window size and position
    window.resizable(True,True)

    main_frame = tk.Frame(window)
    main_frame.pack(fill="both", expand=True)

    # Create instruction label
    instruction_label = tk.Label(main_frame, text="Please choose an option below and enter the corresponding information:")

    # Stores the selected option
    selected_option = tk.StringVar(value="Option 1")

    # Create two radio buttons
    radio_buttons = {}
    radio_buttons["Option 1"] = tk.Radiobutton(main_frame, text="Connect to Another Computer", value="Option 1", variable=selected_option, command=toggle_inputs)
    radio_buttons["Option 2"]= tk.Radiobutton(main_frame, text="Allow Connection to Your Computer", value="Option 2", variable=selected_option, command=toggle_inputs)

    # Create labels
    label1 = tk.Label(main_frame, text="IP Address:")
    label2 = tk.Label(main_frame, text="Port:")
    label3 = tk.Label(main_frame, text="Port:")

    # Create frames for input and error labels
    ip_frame = tk.Frame(main_frame)
    port1_frame = tk.Frame(main_frame)
    port2_frame = tk.Frame(main_frame)

    # Create input and error labels
    entry1 = tk.Entry(ip_frame)
    err_label1 = tk.Label(ip_frame, text="", fg="red")

    entry2 = tk.Entry(port1_frame)
    err_label2 = tk.Label(port1_frame, text="", fg="red")

    entry3 = tk.Entry(port2_frame)
    err_label3 = tk.Label(port2_frame, text="", fg="red")

    # Put input and error labels next to each other
    entry1.grid(row=0, column=0)
    err_label1.grid(row=0, column=1, padx= 10)

    entry2.grid(row=0, column=0)
    err_label2.grid(row=0, column=1, padx= 10)

    entry3.grid(row=0, column=0)
    err_label3.grid(row=0, column=1, padx= 10)

    # # Initial state of inputs (enabled for Option 1)
    toggle_inputs()

    # Create Connect button
    connect_button = tk.Button(main_frame, text="Connect", bg="blue", fg="white", command=click_connect)

    # Place widgets
    instruction_label.pack(anchor="w", pady=10, padx=10)
    radio_buttons["Option 1"].pack(anchor="w", pady=10 , padx=10)
    label1.pack(anchor="w", padx=35)
    ip_frame.pack(anchor="w", padx=35)

    label2.pack(anchor="w", padx=35)
    port1_frame.pack(anchor="w", padx=35)

    radio_buttons["Option 2"].pack(anchor="w", pady=10 , padx=10)
    label3.pack(anchor="w", padx=35)
    port2_frame.pack(anchor="w", padx=35)

    connect_button.pack(anchor="w", pady=20, padx=20)

    # Runs the application
    window.mainloop()