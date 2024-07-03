from pydub import AudioSegment
import simpleaudio as sa
import subprocess

def save_audio_file(audioString : str, fileName : str):
    # Save the response content as an audio file
    with open(fileName, "wb") as f:
        f.write(audioString)

def play_audio_file(fileName : str):
    # Load the audio file using pydub
    audio = AudioSegment.from_file(fileName)
    
    # Play the audio using simpleaudio
    play_obj = sa.play_buffer(
        audio.raw_data,
        num_channels=audio.channels,
        bytes_per_sample=audio.sample_width,
        sample_rate=audio.frame_rate
    )
    
    # Wait for playback to finish before exiting
    play_obj.wait_done()

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

