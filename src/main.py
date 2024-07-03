
import pyaudio
import wave
import keyboard
import time
import os

import llm_model
import llm_utils
import tts_model
import stt_model
import utils
import GLOBALS




def wait_for_prompt():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=GLOBALS.FORMAT, channels=GLOBALS.CHANNELS, rate=GLOBALS.RATE, input=True  , frames_per_buffer=GLOBALS.CHUNK)
    frames = []
    print("Press SPACE to start talking")
    keyboard.wait('space')
    print("Listening... Press SPACE to stop.")
    time.sleep(0.2)
    while True:
        try:
            data = stream.read(GLOBALS.CHUNK)  
            frames.append(data)
        except KeyboardInterrupt:
            break
        if keyboard.is_pressed('space'):
            print("Stoped listening")
            print("Processing...") 
            time.sleep(0.2)
            break   
    stream.stop_stream()
    stream.close()
    audio.terminate()

    wave_file = wave.open(GLOBALS.INPUT_FILE, 'wb')  
    wave_file.setnchannels(GLOBALS.CHANNELS)  
    wave_file.setsampwidth(audio.get_sample_size(GLOBALS.FORMAT))
    wave_file.setframerate(GLOBALS.RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()


def initialize():
    print("Initializing...")
    os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
    llm_utils.is_ollama_active()
    llm_utils.is_mistral_active()

def main():
    initialize()
    alive = True
    while alive   :
        wait_for_prompt()

        print("Converting speech to text...") 
        text = stt_model.transcribe_audio(GLOBALS.INPUT_FILE)

        # if(text.lower() == "exit." or text.lower() == "exit"):
        #     return
          
        print("Brain is thinking...") 
        llm_response = llm_model.get_response_from_prompt(text)
        print(f"Response from LLM: {llm_response}")

        #send to coquoi tts
        print("Converting thought to speech...") 
        output_audio = tts_model.text_to_speech(llm_response)

        utils.save_audio_file(output_audio, GLOBALS.OUTPUT_FILE)

        print("Brain is speaking...") 
        utils.play_audio_file(GLOBALS.OUTPUT_FILE)
    
main()








# start Mistral AI
#     ollama run mistral
# start tts docker image
#     docker run --rm -it -p 5002:5002 --gpus all --entrypoint /bin/bash ghcr.io/coqui-ai/tts
#     python3 TTS/server/server.py --list_models #To get the list of available models
#     python3 TTS/server/server.py --model_name tts_models/en/vctk/vits --use_cuda true
