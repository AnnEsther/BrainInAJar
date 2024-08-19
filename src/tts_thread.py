import threading  # Import threading module for handling threads
import queue  # Import queue module to manage task queues
import GLOBALS  # Import custom module GLOBALS, which contains global variables and settings
import tts_model  # Import custom module tts_model, which handles text-to-speech processing
import utils  # Import custom module utils, which contains utility functions

# Thread class for managing text-to-speech (TTS) tasks
class TTS_Thread(threading.Thread):
    def __init__(self, name, stream_worker):
        super().__init__()
        self.name = name  # Name of the thread
        self.tasks = queue.Queue()  # Queue to hold tasks for the thread
        self._stop_event = threading.Event()  # Event to signal when to stop the thread
        self.stream_worker = stream_worker  # Worker thread responsible for streaming audio output
        self.thread = threading.Thread(target=self.run)  # Initialize the thread with the run method

    # Main loop for the thread that processes tasks
    def run(self):
        while not self._stop_event.is_set():  # Loop until the stop event is set
            try:
                task = self.tasks.get(timeout=1)  # Try to get a task from the queue with a 1-second timeout
                self.send_to_tts(task)  # Process the task
            except queue.Empty:  # If no task is available, continue looping
                continue

    # Method to send a sentence to the text-to-speech model
    def send_to_tts(self, task):
        sentence = task.get('sentence')  # Extract the sentence from the task
        if not sentence:  # If no sentence is provided, log an error and return
            print(f"{self.name} received a task with no prompt.")
            return

        # Check the operating system and handle text-to-speech accordingly
        if GLOBALS.SYS_OS == "Windows":
            response = tts_model.text_to_speech(sentence)  # Convert the sentence to speech on Windows
            self.stream_worker.add_task({"audioBytes": response})  # Send the audio bytes to the stream worker for playback
        else:
            utils.run_command_mac(f'say "{sentence}"')  # On macOS, use the built-in 'say' command to speak the sentence

    # Method to add a task to the thread's queue
    def add_task(self, task):
        self.tasks.put(task)  # Add the task to the queue

    # Method to stop the thread gracefully
    def stop(self):
        self._stop_event.set()  # Set the stop event to signal the thread to stop
        if self.thread.is_alive():  # If the thread is still running, wait for it to finish
            self.thread.join()  # Join the thread, blocking until it has terminated
