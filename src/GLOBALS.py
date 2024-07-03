import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
INPUT_FILE = "input_audio.wav"
OUTPUT_FILE = "output_audio.wav"
LLM_MODEL = "mistral"
TTS_URL = "http://localhost:5002/api/tts"
TTS_PARAMS = {
    "text": "",
    "speaker_id": "p336",
    "style_wav": "",
    "language_id": ""
}