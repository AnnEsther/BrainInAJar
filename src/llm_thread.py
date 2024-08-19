import json  # Import json module for handling JSON data
import threading  # Import threading module to create and manage threads
import queue  # Import queue module to handle tasks in a thread-safe manner
import requests  # Import requests module to send HTTP requests

import GLOBALS  # Import custom module GLOBALS, which contains global variables and settings

# Define a class LLM_Thread that inherits from threading.Thread
class LLM_Thread(threading.Thread):
    def __init__(self, name, tts_worker, ui):
        # Call the constructor of the parent class (threading.Thread)
        super().__init__()
        self.name = name  # Name of the thread for identification
        self.tasks = queue.Queue()  # Queue to manage tasks for the thread
        self._stop_event = threading.Event()  # Event to signal when the thread should stop
        self.tts_worker = tts_worker  # Reference to a text-to-speech worker for handling audio tasks
        self.user_interface = ui  # Reference to a user interface object for displaying text
        self.thread = threading.Thread(target=self.run)  # Create a new thread that will execute the run method

    # Method that contains the main logic of the thread
    def run(self):
        while not self._stop_event.is_set():  # Loop until the stop event is set
            try:
                task = self.tasks.get(timeout=1)  # Wait for a task to be available in the queue, timeout after 1 second
                self.process_task(task)  # Process the retrieved task
            except queue.Empty:  # If no task is available, continue the loop
                continue

    # Method to process each task in the queue
    def process_task(self, task):
        prompt = task.get('prompt')  # Extract the prompt from the task
        if not prompt:  # If no prompt is found, log a message and return
            print(f"{self.name} received a task with no prompt.")
            return
        
        # Send the prompt to the LLM (Language Model) and process the response
        response = self.send_request_to_ollama(prompt)

    # Method to add a new task to the queue
    def add_task(self, task):
        self.tasks.put(task)  # Place the task in the queue for processing

    # Method to stop the thread gracefully
    def stop(self):
        self._stop_event.set()  # Set the stop event to signal the thread to stop
        if self.thread.is_alive():  # If the thread is still running, wait for it to finish
            self.thread.join()

    # Method to send a request to the Ollama API
    def send_request_to_ollama(self, prompt):
        # Define the payload for the API request
        payload = {
            "model": "mistral",  # Specify the model to be used (e.g., "mistral")
            "messages": [
                {
                    "role": "user",
                    "content": prompt  # Include the user's prompt in the request
                }
            ]
        }
        # Send the POST request to the LLM API using the URL and headers defined in GLOBALS
        response = requests.post(GLOBALS.LLM_URL, data=json.dumps(payload), headers=GLOBALS.LLM_HEADERS)
        response.raise_for_status()  # Raise an error if the request was unsuccessful

        actual_response = ""  # Initialize an empty string to accumulate the response
        for line in response.iter_lines():  # Process the response line by line
            if line:
                line_data = json.loads(line.decode('utf-8'))  # Parse the JSON data from the response line
                response_text = line_data.get("message", "")  # Extract the message content
                response_text = response_text.get("content", "")
                self.user_interface.stream_text(response_text)  # Stream the text to the user interface
                
                actual_response += response_text  # Accumulate the response text
                
                # If the response is long enough and contains a period, split it into sentences
                if len(actual_response) > 50 and '.' in actual_response:
                    parts = actual_response.split('.', 1)
                    parts[0] = parts[0] + "."
                    self.tts_worker.add_task({"sentence": parts[0]})  # Send the first part to the TTS worker
                    actual_response = parts[1]  # Keep the remaining part for further processing

                if line_data.get("done", False):  # If the response indicates completion
                    self.tts_worker.add_task({"sentence": actual_response})  # Send the remaining response to the TTS worker
                    break

        self.user_interface.stream_text("\n\n")  # Add some spacing in the user interface
        return actual_response  # Return the complete response
