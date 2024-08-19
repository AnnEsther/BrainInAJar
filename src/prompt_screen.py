import tkinter as tk  # Import the tkinter library for GUI development

import GLOBALS  # Import global settings
import prompt_label  # Import the PromptLabel class

class PromptScreen():
    def __init__(self, root):
        """
        Initialize the PromptScreen.

        Parameters:
        - root: The parent widget (typically a frame or window) where this screen will be placed.
        """
        self.label_frames = []  # List to keep track of label frames

        # Create a top frame to hold the label and text box
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(fill='x', padx=10, pady=10)

        # Create and add a label to the top frame
        self.label = tk.Label(self.top_frame, text='Current Prompt :')
        self.label.pack(side=tk.LEFT, padx=10)

        # Create and add a text box to the top frame
        # The text box is initially disabled to prevent user editing
        self.text_box = tk.Text(self.top_frame, height=1, width=52)
        self.text_box['state'] = 'disabled'
        self.text_box.pack(side=tk.LEFT, padx=10, fill='x', expand=True)

        # Create the parent frame to hold other components
        self.parent_frame = tk.Frame(root)
        self.parent_frame.pack(fill='both', expand=True, pady=10)

        # Create a LabelFrame to organize prompts
        self.labelframe = tk.LabelFrame(self.parent_frame, bg="white", text="Prompts")
        self.labelframe.pack(fill='both', expand=True, padx=10, pady=10)

        # Create a Canvas to display prompt labels with scrolling capability
        self.canvas = tk.Canvas(self.labelframe)
        self.canvas.pack(side=tk.LEFT, fill='both', expand=True)

        # Create and add a vertical scrollbar for the canvas
        self.scrollbar = tk.Scrollbar(self.labelframe, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')

        # Configure canvas to work with the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create a frame inside the canvas to hold prompt labels
        self.table_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        # Create PromptLabel instances for each item in the global boredom prompts list
        for x in GLOBALS.boredom_prompts:
            label_frame = prompt_label.PromptLabel(self.table_frame, x)
            self.label_frames.append(label_frame)

        # Update the scroll region to accommodate the new labels
        self.update_scrollregion()

    def add_text(self, new_text):
        """
        Add new text as a prompt label to the screen.

        Parameters:
        - new_text: The text to be added as a prompt label.
        """
        if new_text:
            label_frame = prompt_label.PromptLabel(self.table_frame, new_text)
            self.label_frames.append(label_frame)
            self.update_scrollregion()

    def update_scrollregion(self):
        """
        Update the canvas scroll region to fit the content.
        """
        self.canvas.update_idletasks()  # Ensure all canvas updates are completed
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  # Set scroll region to include all content

    def highlight_text(self, text_to_highlight):
        """
        Highlight the specified text (by updating the text box).

        Parameters:
        - text_to_highlight: The text to highlight.
        """
        self.update_text(text_to_highlight)

    def remove_label(self, label_frame):
        """
        Remove a specific label from the screen and update global list.

        Parameters:
        - label_frame: The PromptLabel instance to be removed.
        """
        label_frame.destroy()  # Remove the label frame from the GUI
        GLOBALS.boredom_prompts.remove(label_frame.text)  # Remove the prompt text from the global list
        self.label_frames.remove(label_frame)  # Remove the label frame from the list of frames
        self.update_scrollregion()  # Update the scroll region to reflect the removal

    def update_text(self, text):
        """
        Update the text box with new text.

        Parameters:
        - text: The text to be displayed in the text box.
        """
        self.text_box['state'] = 'normal'  # Temporarily enable the text box for editing
        self.text_box.delete("1.0", tk.END)  # Clear existing text
        self.text_box.insert(tk.END, text)  # Insert new text
        self.text_box['state'] = 'disabled'  # Re-disable the text box to prevent editing
