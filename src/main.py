import tkinter as tk

import GLOBALS
import prompt_screen
import input_screen
import output_screen

import ollama_setup
import tts_setup
import audio_thread
import llm_thread
import prompt_thread
import tts_thread
import stream_thread


class AppUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(GLOBALS.APP_NAME)
        self.geometry(GLOBALS.APP_SIZE)

        self.create_components()

        self.start_docker_containers()
        self.create_threads()
        self.start_threads()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_time(self, time_remain):
        self.timer_label.config(text=f"Time Remaining: {time_remain} s")
        
    def highlight_prompt(self, text_to_highlight):
        self.promptScreen.highlight_text(text_to_highlight)

    def stream_text(self,text):
        self.outputScreen.stream_text_to_box(text)
    
    def on_close(self):
        # Custom action on window close
        self.prompt_worker.stop()
        self.llm_worker.stop()
        self.tts_worker.stop()
        self.audio_worker.stop()
        self.stream_worker.stop()
        self.destroy()

    def create_components(self):
        # Parent Frame
        self.parent_frame = tk.Frame(self)
        self.parent_frame.pack(fill='both', expand=True, pady=10)

        self.promptScreen = prompt_screen.PromptScreen( self.parent_frame)

        self.inputScreen = input_screen.InputScreen(self.parent_frame, self.promptScreen)

        self.timer_frame = tk.Frame(self.parent_frame)
        self.timer_frame.pack(padx=10, fill='x', expand=True)
        # Inner frame to center the timer_label and skip_button
        self.inner_frame = tk.Frame(self.timer_frame)
        self.inner_frame.pack()
        self.timer_label = tk.Label(self.inner_frame, text="Timer: ")
        self.timer_label.pack(side=tk.LEFT, padx=10)
        self.skip_button = tk.Button(self.inner_frame, text="Skip", command=self.skip_timer)
        self.skip_button.pack(side=tk.LEFT,padx=10)

        self.outputScreen = output_screen.OutputScreen(self.parent_frame)

    def start_docker_containers(self):
        ollama_setup.start_ollama_container()
        tts_setup.start_tts_container()

    def create_threads(self):
        self.stream_worker = stream_thread.Stream_Thread("stream_thread")
        self.audio_worker = audio_thread.Audio_Thread("audio_thread", streamer = self.stream_worker)
        self.tts_worker = tts_thread.TTS_Thread("tts_thread", stream_worker=self.stream_worker)
        self.llm_worker = llm_thread.LLM_Thread("llm_thread", tts_worker=self.tts_worker,  ui = self)
        self.prompt_worker = prompt_thread.Promt_Thread("prompt_thread", llm_worker=self.llm_worker,interval=60, ui = self)

    def start_threads(self):
        self.audio_worker.start()
        self.tts_worker.start()
        self.llm_worker.start()
        self.prompt_worker.start()
        self.stream_worker.start()

    def skip_timer(self):
        self.prompt_worker.skip_timer()


if __name__ == "__main__":
    app = AppUI()
    app.mainloop()

