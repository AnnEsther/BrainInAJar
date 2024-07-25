import threading
import queue

class Audio_Thread(threading.Thread):
    def __init__(self, name, streamer):
        super().__init__()
        self.name = name
        self.stream_worker = streamer
        self.tasks = queue.Queue()
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self.run)


    def run(self):
        while not self._stop_event.is_set():
            try:
                task = self.tasks.get(timeout=1)  # Wait for a task
                self.process_task(task)
            except queue.Empty:
                continue

    def process_task(self, task):
        output_audio = task.get('audio')
        if not output_audio:
            print(f"{self.name} received a task with no prompt.")
            return
        # Add tasks to the stream thread
        self.stream_worker.add_task({"audioBytes": output_audio})
        # utils.play_audio_from_bytes(output_audio)


    def add_task(self, task):
        self.tasks.put(task)

    def stop(self):
        self._stop_event.set()
        if self.thread.is_alive():
            self.thread.join()

    
