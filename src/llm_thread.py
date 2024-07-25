import json
import threading
import queue
import requests

import GLOBALS

class LLM_Thread(threading.Thread):
    def __init__(self, name, tts_worker, ui):
        super().__init__()
        self.name = name
        self.tasks = queue.Queue()
        self._stop_event = threading.Event()
        self.tts_worker = tts_worker
        self.user_interface = ui
        self.thread = threading.Thread(target=self.run)


    def run(self):
        while not self._stop_event.is_set():
            try:
                task = self.tasks.get(timeout=1)  # Wait for a task
                self.process_task(task)
            except queue.Empty:
                continue

    def process_task(self, task):
        prompt = task.get('prompt')
        if not prompt:
            print(f"{self.name} received a task with no prompt.")
            return
        # print(f"{self.name} sending request with prompt: {prompt}")
        # Send request to Ollama
        response = self.send_request_to_ollama(prompt)

    def add_task(self, task):
        self.tasks.put(task)

    def stop(self):
        self._stop_event.set()
        if self.thread.is_alive():
            self.thread.join()

    def send_request_to_ollama(self,prompt):
        url = "http://localhost:11434/api/generate"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "model": GLOBALS.LLM_MODEL,
            "prompt": prompt
        }

        print(url == GLOBALS.LLM_URL)

        response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)

        # print(response.status_code)
        # print(response.json())
        # return
    
        # GLOBALS.LLM_PAYLOAD["prompt"] = prompt
        # response = requests.post(GLOBALS.LLM_URL, headers=GLOBALS.LLM_HEADERS, data=json.dumps(GLOBALS.LLM_PAYLOAD), stream=True)
        response.raise_for_status()

        actual_response = ""
        for line in response.iter_lines():
            if line:
                line_data = json.loads(line.decode('utf-8'))
                response_text = line_data.get("response", "")
                self.user_interface.stream_text(response_text)
                print(response_text, end="", flush=True)
                actual_response += response_text
                if len(actual_response) > 50 and '.' in actual_response:
                    parts = actual_response.split('.', 1)
                    parts[0] = parts[0] + "."
                    self.tts_worker.add_task({"sentence": parts[0]})
                    actual_response = parts[1]
                if line_data.get("done", False):
                    break
        # print("\n---------------\n")
        self.user_interface.stream_text("\n\n")
        return actual_response


# curl -X POST http://localhost:11434/api/generate -H "Content-Type: application/json" -d '{"model": "mistral", "prompt": "Why is the sky blue?"}'