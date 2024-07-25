import tkinter as tk

import GLOBALS

class InputScreen():
    def __init__(self, root, promptScreen):

        self.propmtScreen = promptScreen
        # Parent Frame , bg = "#d421f4"
        self.main_frame = tk.Frame(root)

        self.text_box = tk.Text(self.main_frame, height = 1, width = 52)
        self.text_box.pack(side=tk.LEFT, padx=10, pady=10, fill='x', expand=True)

        # Create a button
        self.submit_button = tk.Button(self.main_frame, text="Add", command=self.process_text)
        self.submit_button.pack(side=tk.LEFT, padx=10)

        self.main_frame.pack(padx=10, fill='x', expand=True)
    
    def process_text(self):
        # Retrieve the text from the text box
        text = self.text_box.get("1.0", tk.END).strip()  # Get all text from line 1, character 0 to end
        # Call a function with the text
        self.propmtScreen.add_text(text)
        self.text_box.delete("1.0", tk.END)
        GLOBALS.boredom_prompts.append(text)

    def handle_text(self, text):
        # Example function to process the text
        print(f"Received text: {text}")