# gui_manager.py
import tkinter as tk
from tkinter import scrolledtext

class GUIManager:
    def __init__(self, server):
        self.server = server
        self.gui = tk.Tk()
        self.gui.title("Broker mqtt v5")

        self.chat_box = scrolledtext.ScrolledText(self.gui)
        self.chat_box.pack()

        self.button1 = tk.Button(self.gui, text="Button 1", command=lambda: print(1))
        self.button2 = tk.Button(self.gui, text="Button 2", command=lambda: print(2))
        self.button3 = tk.Button(self.gui, text="Button 3", command=lambda: print(3))
        self.button4 = tk.Button(self.gui, text="Button 4", command=lambda: print(4))
        self.button5 = tk.Button(self.gui, text="Quit", command=self.quit_server)

        self.button1.pack()
        self.button2.pack()
        self.button3.pack()
        self.button4.pack()
        self.button5.pack()

        self.server.set_gui_manager(self)

    def update_chat_box(self, message):
        self.chat_box.insert(tk.END, message)

    def check_user(self, name, password):
        # Add your check_user implementation
        return True  # Replace with your actual implementation

    def quit_server(self):
        self.server.quit_server()

    def destroy_gui(self):
        self.gui.destroy()

    def run(self):
        self.gui.mainloop()
