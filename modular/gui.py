import tkinter as tk
from input_widgets import InputWidget
from network import create_socket
from threading import Thread
import utils

class RemoteDesktopGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("TouchPoint - Remote Desktop Connection")
        self.selected_option = tk.StringVar(value="Controller")
        self.initialize_gui()

    def initialize_gui(self):
        self.window.resizable(True, True)

        # Initializes the widgets from the main window
        # Main window
        main_frame = tk.Frame(self.window)

        # Instruction label
        instruction_label = tk.Label(main_frame, text="Please choose an option below and enter the corresponding information:")

        # Input Widgets
        controller_ip = InputWidget(main_frame, "ip", "IP Address:", "Invalid IP address.", "Controller")
        controller_port = InputWidget(main_frame, "port", "Port:", "Invalid port.", "Controller")
        caster_port= InputWidget(main_frame, "port", "Port:", "Invalid port.", "Caster")
        widget_list = [controller_ip, controller_port, caster_port]
        self.toggle_inputs(widget_list)

        # Radio Buttons
        radio_buttons = {}
        radio_buttons["Controller"] = tk.Radiobutton(main_frame, text="Connect to Another Computer", value="Controller", variable=self.selected_option, command=lambda: self.toggle_inputs(widget_list))
        radio_buttons["Caster"]= tk.Radiobutton(main_frame, text="Allow Connection to Your Computer", value="Caster", variable=self.selected_option, command=lambda: self.toggle_inputs(widget_list))

        # Connect button
        connect_button = tk.Button(main_frame, text="Connect", bg="blue", fg="white", command=lambda: self.click_connect(widget_list))

        # Place widgets in main window
        main_frame.pack(fill="both", expand=True)

        instruction_label.pack(anchor="w", pady=10, padx=10)
        radio_buttons["Controller"].pack(anchor="w", pady=10 , padx=10)
        controller_ip.place_widget()
        controller_port.place_widget()

        radio_buttons["Caster"].pack(anchor="w", pady=10 , padx=10)
        caster_port.child_frame.pack(anchor="w", padx=35)
        caster_port.place_widget()

        connect_button.pack(anchor="w", pady=20, padx=20)

    def click_connect(self, input_widgets):
    
    def validate_entries(input_widgets):
        validation_map = {
            "ip": utils.is_valid_ip,
            "port": utils.is_valid_port
        }

        for widget in input_widgets:
            if widget.entry.cget("state") != "normal":
                continue

            validation_func = validation_map.get(widget.type)
            if not validation_func:
                raise ValueError(f"Unsupported widget type: {widget.type}")

            if not validation_func(widget.get_entry()):
                return False

        return True

    def start_client(self, ip, port):
        Thread(target=self.client_handler, args=(ip, port)).start()

    def start_server(self, ip, port):
        Thread(target=self.server_handler, args=(ip, port)).start()

    def client_handler(self, ip, port):
        # Import and call controller logic here
        pass

    def server_handler(self, ip, port):
        # Import and call caster logic here
        pass

    def toggle_inputs(self, input_widgets):
        for widget in input_widgets:
            widget.update_err_label("")
            if self.selected_option.get() == widget.option:
                widget.enable()
            else:
                widget.disable()

    def run(self):
        self.window.mainloop()

gui = RemoteDesktopGUI()
gui.run()