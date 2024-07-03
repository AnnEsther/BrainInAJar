import requests
import GLOBALS

def text_to_speech (text:str):
    # Define the API endpoint and parameters
    GLOBALS.TTS_PARAMS["text"] = text
   
    # Make the GET request
    response = requests.get(GLOBALS.TTS_URL, params=GLOBALS.TTS_PARAMS)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response
        # print("Response received:")
        # print(response.content)

        return response.content
    else:
        # Handle the error
        print(f"Error: {response.status_code}")
        print(response.text)