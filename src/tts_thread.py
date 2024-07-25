import threading
import queue
import tts_model

class TTS_Thread(threading.Thread):
    def __init__(self, name, stream_worker):
        super().__init__()
        self.name = name
        self.tasks = queue.Queue()
        self._stop_event = threading.Event()
        self.stream_worker = stream_worker
        self.thread = threading.Thread(target=self.run)


    def run(self):
        while not self._stop_event.is_set():
            try:
                task = self.tasks.get(timeout=1)  # Wait for a task
                self.send_to_tts(task)
            except queue.Empty:
                continue

    def send_to_tts(self, task):
        sentence = task.get('sentence')
        if not sentence:
            print(f"{self.name} received a task with no prompt.")
            return
        # print(f"{self.name} sending sentence with prompt: {prompt}")
        # Send request to Ollama
        # response = asyncio.run(llm_model.send_request_to_ollama(prompt))
        response = tts_model.text_to_speech(sentence)
        #send response to audio player
        # self.audio_worker.add_task({"audio": response})
        self.stream_worker.add_task({"audioBytes": response})

    def add_task(self, task):
        self.tasks.put(task)

    def stop(self):
        self._stop_event.set()
        if self.thread.is_alive():
            self.thread.join()

