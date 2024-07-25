import queue
import threading
import pyaudio
import GLOBALS


class Stream_Thread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.tasks = queue.Queue()
        self.thread = threading.Thread(target=self.run)
        # self.thread.daemon = True  # Daemonize thread to exit when main program exits
        self.stop_event = threading.Event()

    def run(self):
        # Initialize PyAudio
        self.pyAud = pyaudio.PyAudio()
        # Open stream
        self.stream = self.pyAud.open(format=GLOBALS.STREAM_FORMAT, channels=GLOBALS.STREAM_CHANNELS, rate=GLOBALS.STREAM_RATE,  output=True)
        while not self.stop_event.is_set():
            try:
                task = self.tasks.get(timeout=1)  # Wait for a task
                self.process_task(task)
            except queue.Empty:
                continue

    def process_task(self, task):
        audio_bytes = task.get('audioBytes')
        if not audio_bytes:
            print(f"{self.name} received a task with no prompt.")
            return
        # Play audio data
        self.stream.write(audio_bytes)
        

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        if self.thread.is_alive():
            self.thread.join()        
        # Stop stream
        self.stream.stop_stream()
        self.stream.close()
        # Terminate PyAudio
        self.pyAud.terminate()




        

    def add_task(self, task):
        self.tasks.put(task)
