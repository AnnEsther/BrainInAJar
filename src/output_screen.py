import tkinter as tk  # Import the tkinter library for GUI development
from tkinter import scrolledtext  # Import scrolledtext for a text widget with a scrollbar

class OutputScreen():
    def __init__(self, root):
        """
        Initialize the OutputScreen.

        Parameters:
        - root: The parent widget (typically a frame or window) where this screen will be placed.
        """
        # Create the main frame for this screen
        self.main_frame = tk.Frame(root)

        # Create a ScrolledText widget to display streamed text
        # ScrolledText provides a text area with a scrollbar
        self.stream_text = scrolledtext.ScrolledText(self.main_frame, width=52, height=25)
        self.stream_text.pack(padx=10, pady=10, fill='x', expand=True)

        # Pack the main frame into the parent widget
        self.main_frame.pack(pady=10, padx=10, fill='x', expand=True)

    def stream_text_to_box(self, text):
        """
        Insert text into the ScrolledText widget and ensure the latest text is visible.

        Parameters:
        - text: The text to be added to the ScrolledText widget.
        """
        self.stream_text.insert(tk.END, text)  # Insert text at the end of the widget
        self.stream_text.yview(tk.END)  # Scroll to the end of the text to make it visible

    def clear_stream_text(self):
        """
        Clear all text from the ScrolledText widget.
        """
        self.stream_text.delete(1.0, tk.END)  # Delete all text from the beginning to the end
