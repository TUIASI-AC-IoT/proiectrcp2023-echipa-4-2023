# gui_manager.py
import tkinter as tk
from tkinter import scrolledtext
from encoder import generate_disconnect_packet

class GUIManager:
    def __init__(self, server):
        self.server = server
        self.gui = tk.Tk()
        self.gui.title("Broker mqtt v5")

        self.chat_box = scrolledtext.ScrolledText(self.gui)
        self.chat_box.pack()

        self.button1 = tk.Button(self.gui, text="Topic History", command=self.topics_subcribed)
        self.button2 = tk.Button(self.gui, text="Visualize Messages", command=self.last10_mesajes)
        self.button3 = tk.Button(self.gui, text="Visualize Clients  History", command=lambda: print(3))
        self.button4 = tk.Button(self.gui, text="Visualize Qos Messages", command=self.qos_print)
        self.button5 = tk.Button(self.gui, text="Quit", command=self.quit_server)

        self.button1.pack()
        self.button2.pack()
        self.button3.pack()
        self.button4.pack()
        self.button5.pack()

        self.server.set_gui_manager(self)

    def update_chat_box(self, message):
        self.chat_box.insert(tk.END, message)

    def quit_server(self):
        self.server.quit_server()
    def qos_print(self):
        self.server.print_qos_messages()
    def last10_mesajes(self):
        self.server.visualize_mesages()

    def topics_subcribed(self):
        self.server.visualize_topics()

    def destroy_gui(self):
        self.gui.destroy()

    def run(self):
        self.gui.mainloop()
