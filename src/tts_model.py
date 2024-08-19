import requests  # Import requests module to make HTTP requests
import GLOBALS  # Import custom module GLOBALS, which contains global variables and settings

# Function to convert text to speech using an external API
def text_to_speech(text: str):
    # Update the text parameter in the GLOBALS.TTS_PARAMS dictionary with the input text
    GLOBALS.TTS_PARAMS["text"] = text
   
    # Make a GET request to the text-to-speech API with the updated parameters
    response = requests.get(GLOBALS.TTS_URL, params=GLOBALS.TTS_PARAMS)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code ==
