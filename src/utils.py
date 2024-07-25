import pyaudio
# from pydub import AudioSegment
# import simpleaudio as sa
import subprocess
import time


def save_audio_file(audioString : str, fileName : str):
    # Save the response content as an audio file
    with open(fileName, "wb") as f:
        f.write(audioString)

# def play_audio_file(fileName : str):
#     # Load the audio file using pydub
#     audio = AudioSegment.from_file(fileName)
    
#     # Play the audio using simpleaudio
#     play_obj = sa.play_buffer(
#         audio.raw_data,
#         num_channels=audio.channels,
#         bytes_per_sample=audio.sample_width,
#         sample_rate=audio.frame_rate
#     )
    
#     # Wait for playback to finish before exiting
#     play_obj.wait_done()

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
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    time_taken = end_time - start_time
    return result, time_taken

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

def run_command_mac(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if process.returncode == 0:
        print(f"Command '{command}' executed successfully.")
        print("Output:\n" + stdout.decode())
    else:
        print(f"Command '{command}' failed with return code {process.returncode}.")
        print("Error:\n" + stderr.decode())