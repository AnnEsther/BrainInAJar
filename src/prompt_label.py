import tkinter as tk  # Import the tkinter library for GUI development

import GLOBALS  # Import global settings

class PromptLabel():
    text = ""  # Class-level variable to store the prompt text

    def __init__(self, root, prompt):
        """
        Initialize the PromptLabel.

        Parameters:
        - root: The parent widget (typically a frame or window) where this label will be placed.
        - prompt: The text to be displayed in the label.
        """
        self.text = prompt  # Store the prompt text

        # Create a frame to hold the label and the close button
        self.label_frame = tk.Frame(root)

        # Create a label with the prompt text
        # `anchor='w'` aligns the text to the west (left) side of the label
        # `width=83` sets the width of the label
        label = tk.Label(self.label_frame, text=prompt, anchor='w', width=83)
        label.pack(side=tk.LEFT, fill='x', expand=True)

        # Create a close button to remove the label
        # `lambda : self.remove_label()` calls the `remove_label` method when the button is clicked
        close_button = tk.Button(self.label_frame, text="x", command=lambda: self.remove_label())
        close_button.pack(side=tk.RIGHT)

        # Pack the label frame into the parent widget
        self.label_frame.pack(fill='x', pady=2, expand=True)

    def remove_label(self):
        """
        Remove the label from the GUI and update the global list of boredom prompts.
        """
        self.label_frame.destroy()  # Destroy the label frame
        GLOBALS.boredom_prompts.remove(self.text)  # Remove the prompt text from the global list

    def highlight_text(self):
        """
        Change the background color of the label frame to highlight it.
        """
        self.label_frame.config(bg="#0564e2")  # Set the background color to a highlight color
