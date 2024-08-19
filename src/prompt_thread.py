import threading  # Import threading module to handle multi-threaded tasks
import time  # Import time module to handle timing operations
import random  # Import random module to choose random items
import GLOBALS  # Import custom module GLOBALS, which contains global variables and settings

# Class to handle periodic sending of prompts in a separate thread
class Promt_Thread(threading.Thread):
    def __init__(self, name, llm_worker, interval, ui):
        super().__init__()
        self.name = name  # Name of the thread
        self.llm_worker = llm_worker  # Reference to the LLM worker thread for handling prompts
        self.interval = interval  # Interval between prompt executions in seconds
        self.thread = threading.Thread(target=self.run)  # Create a new thread targeting the run method
        self.thread.daemon = True  # Daemonize the thread so it exits when the main program exits
        self.stop_event = threading.Event()  # Event to control stopping the thread
        self.user_interface = ui  # Reference to the user interface for updating prompts and time

    # Method to select a random prompt and send it to the LLM worker thread
    def send_prompt(self):
        prompt = random.choice(GLOBALS.boredom_prompts)  # Select a random prompt from the list in GLOBALS
        self.user_interface.highlight_prompt(prompt)  # Highlight the selected prompt in the UI
        # Add the prompt as a task to the LLM worker thread
        self.llm_worker.add_task({"prompt": prompt + GLOBALS.condition})

    # Method that runs in the thread and periodically sends prompts
    def run(self):
        self.start_time = time.time()  # Record the start time when the thread starts
        while not self.stop_event.is_set():  # Continue running until the stop event is set
            current_time = time.time()  # Get the current time
            elapsed_time = current_time - self.start_time  # Calculate elapsed time since the last prompt
            # Update the UI with the remaining time until the next prompt
            self.user_interface.update_time(round(self.interval - elapsed_time))
            if elapsed_time >= self.interval:  # If the elapsed time has reached the interval
                self.send_prompt()  # Send a new prompt
                self.start_time = current_time  # Reset the start time
            time.sleep(1)  # Sleep for 1 second to control the loop timing

    # Method to start the thread
    def start(self):
        self.thread.start()  # Start the thread to begin running the run method

    # Method to stop the thread
    def stop(self):
        self.stop_event.set()  # Set the stop event to exit the loop
        if self.thread.is_alive():  # Check if the thread is still running
            self.thread.join()  # Wait for the thread to finish execution

    # Method to skip the timer and send a prompt immediately
    def skip_timer(self):
        self.start_time = time.time() - self.interval  # Adjust start time to trigger prompt sending
