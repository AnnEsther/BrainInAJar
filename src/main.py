import tkinter as tk  # Import the tkinter library for GUI development

# Importing modules for global settings, screen management, threading, and utilities
import GLOBALS
import prompt_screen
import input_screen
import output_screen

import llm_thread
import prompt_thread
import tts_thread
import stream_thread
import utils

class AppUI(tk.Tk):
    def __init__(self):
        """
        Initialize the application user interface.
        """
        super().__init__()  # Call the parent class (tk.Tk) initializer
        self.title(GLOBALS.APP_NAME)  # Set the window title from global settings
        self.geometry(GLOBALS.APP_SIZE)  # Set the window size from global settings

        self.create_components()  # Create GUI components
        utils.initiate_enviornment()  # Initialize environment settings

        self.create_threads()  # Create background threads
        self.start_threads()  # Start the background threads

        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle window close event

    def update_time(self, time_remain):
        """
        Update the timer label with the remaining time.
        """
        self.timer_label.config(text=f"Time Remaining: {time_remain} s")

    def highlight_prompt(self, text_to_highlight):
        """
        Highlight text in the prompt screen.
        """
        self.promptScreen.highlight_text(text_to_highlight)

    def stream_text(self, text):
        """
        Stream text to the output screen.
        """
        self.outputScreen.stream_text_to_box(text)

    def on_close(self):
        """
        Actions to perform when the window is closed.
        """
        # Stop all worker threads
        self.prompt_worker.stop()
        self.llm_worker.stop()
        self.tts_worker.stop()
        if GLOBALS.SYS_OS == "Windows":
            self.stream_worker.stop()  # Stop the stream worker if on Windows
        self.destroy()  # Close the application window

    def create_components(self):
        """
        Create and layout GUI components.
        """
        # Create a parent frame to hold other components
        self.parent_frame = tk.Frame(self)
        self.parent_frame.pack(fill='both', expand=True, pady=10)

        # Create and add screens to the parent frame
        self.promptScreen = prompt_screen.PromptScreen(self.parent_frame)
        self.inputScreen = input_screen.InputScreen(self.parent_frame, self.promptScreen)

        # Create a frame for the timer and skip button
        self.timer_frame = tk.Frame(self.parent_frame)
        self.timer_frame.pack(padx=10, fill='x', expand=True)

        # Inner frame to center the timer label and skip button
        self.inner_frame = tk.Frame(self.timer_frame)
        self.inner_frame.pack()
        self.timer_label = tk.Label(self.inner_frame, text="Timer: ")
        self.timer_label.pack(side=tk.LEFT, padx=10)
        self.skip_button = tk.Button(self.inner_frame, text="Skip", command=self.skip_timer)
        self.skip_button.pack(side=tk.LEFT, padx=10)

        # Create and add the output screen
        self.outputScreen = output_screen.OutputScreen(self.parent_frame)

    def create_threads(self):
        """
        Create background threads for different tasks.
        """
        if GLOBALS.SYS_OS == "Windows":
            self.stream_worker = stream_thread.Stream_Thread("stream_thread")
            self.tts_worker = tts_thread.TTS_Thread("tts_thread", stream_worker=self.stream_worker)
        else:
            self.tts_worker = tts_thread.TTS_Thread("tts_thread", stream_worker=[])
        self.llm_worker = llm_thread.LLM_Thread("llm_thread", tts_worker=self.tts_worker, ui=self)
        self.prompt_worker = prompt_thread.Promt_Thread("prompt_thread", llm_worker=self.llm_worker, interval=60, ui=self)

    def start_threads(self):
        """
        Start all background threads.
        """
        self.tts_worker.start()
        self.llm_worker.start()
        self.prompt_worker.start()
        if GLOBALS.SYS_OS == "Windows":
            self.stream_worker.start()

    def skip_timer(self):
        """
        Skip the timer in the prompt worker.
        """
        self.prompt_worker.skip_timer()

# Entry point of the application
if __name__ == "__main__":
    app = AppUI()  # Create an instance of the AppUI class
    app.mainloop()  # Start the Tkinter event loop
