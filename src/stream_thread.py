import queue  # Import queue module to handle task queues
import threading  # Import threading module to handle multi-threaded tasks
import pyaudio  # Import pyaudio for handling audio streams
import GLOBALS  # Import custom module GLOBALS, which contains global variables and settings
import utils  # Import custom module utils, which contains utility functions

# Class to handle audio streaming in a separate thread
class Stream_Thread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name  # Name of the thread
        self.tasks = queue.Queue()  # Queue to hold tasks for processing
        self.thread = threading.Thread(target=self.run)  # Create a new thread targeting the run method
        self.stop_event = threading.Event()  # Event to control stopping the thread

    # Method that runs in the thread and handles audio streaming
    def run(self):
        # Initialize PyAudio to manage audio input/output
        self.pyAud = pyaudio.PyAudio()
        # Open an audio stream for output with settings from GLOBALS
        self.stream = self.pyAud.open(
            format=GLOBALS.STREAM_FORMAT,  # Audio format (e.g., sample size)
            channels=GLOBALS.STREAM_CHANNELS,  # Number of audio channels
            rate=GLOBALS.STREAM_RATE,  # Sampling rate
            output=True  # Set stream to output mode
        )
        while not self.stop_event.is_set():  # Continue running until the stop event is set
            try:
                # Wait for a task from the queue with a timeout of 1 second
                task = self.tasks.get(timeout=1)
                self.process_task(task)  # Process the task
            except queue.Empty:
                continue  # Continue the loop if the queue is empty

    # Method to process each task in the queue
    def process_task(self, task):
        # Get audio bytes from the task
        audio_bytes = task.get('audioBytes')
        if not audio_bytes:  # If there's no audio data, print a warning
            print(f"{self.name} received a task with no prompt.")
            return
        # Play the audio data through the stream
        self.stream.write(audio_bytes)

    # Method to start the thread
    def start(self):
        self.thread.start()  # Start the thread to begin running the run method

    # Method to stop the thread and clean up resources
    def stop(self):
        self.stop_event.set()  # Set the stop event to exit the loop
        if self.thread.is_alive():  # Check if the thread is still running
            self.thread.join()  # Wait for the thread to finish execution
        # Stop the audio stream
        self.stream.stop_stream()
        self.stream.close()
        # Terminate PyAudio to release resources
        self.pyAud.terminate()

    # Method to add tasks to the queue
    def add_task(self, task):
        self.tasks.put(task)  # Put the task in the queue for processing
