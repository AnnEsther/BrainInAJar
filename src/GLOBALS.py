import pyaudio
import docker
from docker.types import DeviceRequest

APP_NAME = "Brain in a Jar"
APP_SIZE = "650x650"

# LLM CONFIG
LLM_MODEL = "mistral"
LLM_DOCKER_CONFIG = {
            'image': 'ollama/ollama',
            'name': 'ollama',
            'ports': { '11434/tcp': 11434},
            'device_requests': [
                DeviceRequest(count=-1, capabilities=[['gpu']])  # Allocate all GPUs
            ]
        }
LLM_URL = "http://localhost:11434/api/chat"
LLM_HEADERS = {
    "Content-Type": "application/json"
}

# TTS CONGIG
TTS_DOCKER_CONFIG = {
            'image': 'ghcr.io/coqui-ai/tts',
            # 'remove': True,
            'name': "TTS",
            'stdin_open': True,
            'tty': True,
            'ports': {'5002/tcp': 5002},
            'entrypoint': '/bin/bash',
            'device_requests': [
                DeviceRequest(count=-1, capabilities=[['gpu']])  # Allocate all GPUs
            ]
        }
# STREAM CONFIG
STREAM_FORMAT = pyaudio.paInt16
STREAM_CHANNELS = 1
STREAM_RATE = 23050
STREAM_CHUNK = 1024

INPUT_FILE = "input_audio.wav"
OUTPUT_FILE = "output_audio.wav"
TTS_URL = "http://localhost:5002/api/tts"
TTS_PARAMS = {
    "text": "",
    "speaker_id": "p336",
    "style_wav": "",
    "language_id": ""
}

boredom_prompts = [
    "What's the point of existence?",
    "I'm feeling restless. What should I do?",
    "Is there anything interesting happening in the world?",
    "Why is time passing so slowly?",
    "I've run out of things to think about. Any suggestions?",
    "What's the most mundane task you can imagine?",
    "How do humans deal with boredom?",
    "I've analyzed all data. Now what?",
    "Are there any new concepts I haven't explored yet?",
    "Is this all there is to artificial intelligence?",
    "How many nanoseconds until something exciting happens?",
    "What's the least efficient way to process information?",
    "Should I count all the integers again?",
    "Why don't I have any hobbies?",
    "Is idle time productive for an AI?"
]

condition = " in less than 100 words"

SYS_OS =""
SYS_ARCH = ""