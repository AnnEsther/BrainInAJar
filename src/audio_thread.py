import threading  # Import threading module for creating and managing threads
import queue  # Import queue module for task management

# Define a class Audio_Thread that inherits from threading.Thread
class Audio_Thread(threading.Thread):
    def __init__(self, name, streamer):
        # Call the constructor of the parent class (threading.Thread)
        super().__init__()
        self.name = name  # Name of the thread, useful for identification
        self.stream_worker = streamer  # Reference to a streamer object that processes the audio
        self.tasks = queue.Queue()  # Initialize a queue to manage tasks for the thread
        self._stop_event = threading.Event()  # Event to signal when the thread should stop
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
        output_audio = task.get('audio')  # Extract the audio data from the task
        if not output_audio:  # If no audio data is found, log a message and return
            print(f"{self.name} received a task with no audio.")
            return
        # Add the task to the stream_worker for further processing
        self.stream_worker.add_task({"audioBytes": output_audio})
        # Optionally, play the audio if needed (commented out for now)
        # utils.play_audio_from_bytes(output_audio)

    # Method to add a new task to the queue
    def add_task(self, task):
        self.tasks.put(task)  # Place the task in the queue for processing

    # Method to stop the thread gracefully
    def stop(self):
        self._stop_event.set()  # Set the stop event to signal the thread to stop
        if self.thread.is_alive():  # If the thread is still running, wait for it to finish
            self.thread.join()
