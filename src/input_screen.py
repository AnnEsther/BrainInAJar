import tkinter as tk  # Import the tkinter library for GUI development

import GLOBALS  # Import global settings

class InputScreen():
    def __init__(self, root, promptScreen):
        """
        Initialize the InputScreen.
        
        Parameters:
        - root: The parent widget (typically a frame or window) where this screen will be placed.
        - promptScreen: An instance of the PromptScreen class used to interact with.
        """
        self.propmtScreen = promptScreen  # Store reference to the PromptScreen instance
        
        # Create the main frame for this screen
        self.main_frame = tk.Frame(root)

        # Create a text box for user input with specific dimensions
        self.text_box = tk.Text(self.main_frame, height=1, width=52)
        self.text_box.pack(side=tk.LEFT, padx=10, pady=10, fill='x', expand=True)

        # Create a button to submit the text
        self.submit_button = tk.Button(self.main_frame, text="Add", command=self.process_text)
        self.submit_button.pack(side=tk.LEFT, padx=10)

        # Pack the main frame into the parent widget
        self.main_frame.pack(padx=10, fill='x', expand=True)

    def process_text(self):
        """
        Process the text input by the user.
        Retrieves the text from the text box, sends it to the PromptScreen, 
        clears the text box, and appends the text to the global boredom prompts list.
        """
        # Retrieve the text from the text box, strip leading/trailing whitespace
        text = self.text_box.get("1.0", tk.END).strip()  # Get all text from line 1, character 0 to end
        # Pass the text to the PromptScreen's add_text method
        self.propmtScreen.add_text(text)
        # Clear the text box
        self.text_box.delete("1.0", tk.END)
        # Add the text to the global boredom prompts list
        GLOBALS.boredom_prompts.append(text)

    def handle_text(self, text):
        """
        Example function to handle text (for debugging or processing).
        
        Parameters:
        - text: The text to process.
        """
        print(f"Received text: {text}")  # Print the received text to the console
