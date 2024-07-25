import tkinter as tk

import GLOBALS
import prompt_label


class PromptScreen():
    def __init__(self, root):

        self.label_frames = []

       # Create a frame to hold the label and text box
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(fill='x', padx=10, pady=10)

        # Label
        self.label = tk.Label(self.top_frame, text='Current Prompt :')
        self.label.pack(side=tk.LEFT, padx=10)

        # Text box
        self.text_box = tk.Text(self.top_frame, height=1, width=52)
        self.text_box['state'] = 'disabled'
        self.text_box.pack(side=tk.LEFT, padx=10, fill='x', expand=True)

        # Parent Frame
        self.parent_frame = tk.Frame(root)
        self.parent_frame.pack(fill='both', expand=True, pady=10)


        # LabelFrame
        self.labelframe = tk.LabelFrame(self.parent_frame, bg="white",  text="Prompts")
        self.labelframe.pack(fill='both', expand=True, padx=10, pady=10)


        # Canvas
        self.canvas = tk.Canvas(self.labelframe)
        self.canvas.pack(side=tk.LEFT, fill='both', expand=True)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(self.labelframe, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')

        # Configure Canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        # self.canvas.bind('<Configure>', self.on_canvas_configure)

        # Frame inside Canvas , bg = "orange"
        self.table_frame = tk.Frame(self.canvas)
        # self.table_frame.pack(fill='x', pady=2, expand=True)
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        
        for x in GLOBALS.boredom_prompts:
            label_frame = prompt_label.PromptLabel(self.table_frame, x)
            self.label_frames.append(label_frame)
        self.update_scrollregion()


    def add_text(self, new_text):
        if new_text:
            label_frame = prompt_label.PromptLabel(self.table_frame, new_text)
            self.label_frames.append(label_frame)
            self.update_scrollregion()

    def update_scrollregion(self):
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


    def highlight_text(self, text_to_highlight):
        self.update_text(text_to_highlight)

    def remove_label(self, label_frame):
        label_frame.destroy()
        GLOBALS.boredom_prompts.remove(label_frame.text)
        self.label_frames.remove(label_frame)
        self.update_scrollregion()

    def update_text(self, text):
        # Temporarily set the text box state to normal to update the text
        self.text_box['state'] = 'normal'
        self.text_box.delete("1.0", tk.END)  # Clear existing text
        self.text_box.insert(tk.END, text)  # Insert new text
        self.text_box['state'] = 'disabled'  # Set state back to disabled
