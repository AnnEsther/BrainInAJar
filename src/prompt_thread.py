import threading
import time
import random
import GLOBALS

# def send_prompt(llm_worker):
#     prompt = random.choice(boredom_prompts)
#     print(f"Boredom prompt: {prompt}")
#     # Add tasks to the worker thread
#     llm_worker.add_task({"prompt": prompt})

# def prompt_sender(llm_worker):
#     while True:
#         send_prompt(llm_worker)
#         time.sleep(60)  # Sleep for 1 minute

class Promt_Thread(threading.Thread):
    def __init__(self, name,llm_worker, interval, ui):
        super().__init__()
        self.name = name
        self.llm_worker = llm_worker
        self.interval = interval  # Interval between executions in seconds
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True  # Daemonize thread to exit when main program exits
        self.stop_event = threading.Event()
        self.user_interface = ui

    def send_prompt(self):
        prompt = random.choice(GLOBALS.boredom_prompts)
        self.user_interface.highlight_prompt(prompt)
        # print(f"\nBoredom prompt: {prompt}")
        # print("--------------\n")
        # Add tasks to the worker thread
        self.llm_worker.add_task({"prompt": prompt + GLOBALS.condition})

    def run(self):
        self.start_time = time.time()  # Record the start time
        while not self.stop_event.is_set():
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            # print(round(self.interval - elapsed_time))
            self.user_interface.update_time(round(self.interval - elapsed_time))
            if elapsed_time >= self.interval:
                self.send_prompt()
                self.start_time = current_time  # Reset the start time
            time.sleep(1)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        if self.thread.is_alive():
            self.thread.join()
    
    def skip_timer(self):
        self.start_time = time.time() - self.interval
