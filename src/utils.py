import platform  # Import platform module to get information about the OS
import pyaudio  # Import PyAudio module to handle audio playback
import subprocess  # Import subprocess module to run system commands
import time  # Import time module to measure execution time

import GLOBALS  # Import custom module GLOBALS, which contains global variables and settings
import ollama_setup  # Import custom module ollama_setup, which handles setup for the Ollama container
import tts_setup  # Import custom module tts_setup, which handles setup for the TTS container

# Function to save audio data to a file
def save_audio_file(audioString : str, fileName : str):
    # Save the response content as an audio file
    with open(fileName, "wb") as f:
        f.write(audioString)

# Function to run a system command in the command prompt
def run_command(command):
    """
    Run a command in the command prompt.

    Args:
        command (str): The command to run.

    Returns:
        str: The standard output from the command.
    """
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"Command output: {e.output}")
        return None

# Function to measure the time taken by another function to execute
def measure_time(func, *args, **kwargs):
    """
    Measure the time taken by a function to execute.

    Args:
        func (callable): The function to measure.
        *args: Arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        tuple: The result of the function and the time taken to execute.
    """
    start_time = time.time()  # Record the start time
    result = func(*args, **kwargs)  # Call the function with provided arguments
    end_time = time.time()  # Record the end time
    time_taken = end_time - start_time  # Calculate the time taken
    return result, time_taken

# Function to play audio directly from byte data using PyAudio
def play_audio_from_bytes(audio_bytes):
    chunk = 1024  # Chunk size for audio stream
    format = pyaudio.paInt16  # Audio format (16-bit PCM)
    channels = 1  # Number of audio channels (1 for mono, 2 for stereo)
    rate = 23050  # Sample rate (samples per second)

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    output=True)

    # Play audio data
    stream.write(audio_bytes)

    # Stop stream
    stream.stop_stream()
    stream.close()

    # Terminate PyAudio
    p.terminate()

# Function to run a command on macOS
def run_command_mac(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if process.returncode == 0:
        print(f"Command '{command}' executed successfully.")
        print("Output:\n" + stdout.decode())
    else:
        print(f"Command '{command}' failed with return code {process.returncode}.")
        print("Error:\n" + stderr.decode())

# Function to check if a program is installed on the system
def is_installed(program):
    try:
        result = subprocess.run([program, '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            return False
    except FileNotFoundError:
        return False

# Function to initiate the environment based on the operating system
def initiate_enviornment():
    os_name = platform.system()  # Get the name of the operating system
    GLOBALS.SYS_OS = os_name  # Store the OS name in the global settings
    if os_name == "Windows":
        if is_installed('docker'):  # Check if Docker is installed
            ollama_setup.start_ollama_container()  # Start the Ollama container if Docker is installed
            tts_setup.start_tts_container()  # Start the TTS container if Docker is installed
        else:
            print("Install Docker first.")
    else:
        if is_installed('ollama'):  # Check if Ollama is installed
            ollama_setup.start_ollama()  # Start Ollama directly if installed
        else:
            print("Install Ollama first.")
