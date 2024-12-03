import tkinter as tk

class InputWidget:
    def __init__(self, parent_frame, entry_type, label_text, err_prompt, option):
        self.child_frame = tk.Frame(parent_frame)
        self.entry_type = entry_type.strip().lower()
        self.label = tk.Label(self.child_frame, text=label_text)
        self.entry = tk.Entry(self.child_frame)
        self.err_label = tk.Label(self.child_frame, text=err_prompt, fg="red")
        self.option = option

    def place_widget(self):
        self.label.grid(row=0, column=0, sticky="w")
        self.entry.grid(row=1, column=0)
        self.err_label.grid(row=1, column=1, padx= 10)
        self.child_frame.pack(anchor="w", padx=35)

    def get_entry(self):
        return self.entry.get()
    
    def clear_entry(self):
        self.entry.delete(0, tk.END)

    def update_err_label(self, new_prompt):
        self.err_label.configure(text=new_prompt)

    def enable(self):
        self.label.configure(state="normal")
        self.entry.configure(state="normal")
        self.update_err_label("")

    def disable(self):
        self.label.configure(state="disabled")
        self.entry.configure(state="disabled")
        self.update_err_label("")