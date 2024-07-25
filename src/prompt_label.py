import tkinter as tk

import GLOBALS

class PromptLabel():
    text = ""
    def __init__(self, root, prompt):
        self.text = prompt
        # , bg = "#d4f1f4"
        self.label_frame = tk.Frame(root)

        # , bg = "#d4f1f4"
        label = tk.Label(self.label_frame, text=prompt, anchor='w', width=83)
        label.pack(side=tk.LEFT, fill='x', expand=True)

        close_button = tk.Button(self.label_frame, text="x", command=lambda : self.remove_label())
        close_button.pack(side=tk.RIGHT)

        self.label_frame.pack(fill='x', pady=2, expand=True)

    def remove_label(self):
        self.label_frame.destroy()
        GLOBALS.boredom_prompts.remove(self.text)

    def highlight_text(self):
        self.label_frame.config(bg="#0564e2")