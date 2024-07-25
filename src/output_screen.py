import tkinter as tk
from tkinter import scrolledtext

class OutputScreen():
    def __init__(self, root):

        # Parent Frame , bg = "#d428f4"
        self.main_frame = tk.Frame(root)

        self.stream_text = scrolledtext.ScrolledText(self.main_frame, width=52, height=25)
        self.stream_text.pack(padx=10, pady=10, fill='x', expand=True)

        self.main_frame.pack(pady=10, padx=10, fill='x', expand=True)
    
    def stream_text_to_box(self, text):
        self.stream_text.insert(tk.END, text)
        self.stream_text.yview(tk.END)

    def clear_stream_text(self):
        self.stream_text.delete(1.0, tk.END)