import os
import requests
# ... other imports ...

SPEAKER_WAV_PATH = "/home/ben/reference_speaker.wav" 
OUTPUT_WAV_PATH = "/home/ben/api_output.wav"

data = {
    "text": "This message was generated using a local API server on a dedicated Linux machine.",
    "language": "en" 
}

files = {
    'speaker_wav': (os.path.basename(SPEAKER_WAV_PATH), 
                    open(SPEAKER_WAV_PATH, 'rb'), 
                    'audio/wav') # Ensure the mime type is simple and correct
}

try:
    print(f"Sending request for: '{data['text'][:40]}...'")
    
    # Send the request
    # Use 'with' to ensure the file object is closed even if the request fails
    with open(SPEAKER_WAV_PATH, 'rb') as audio_file:
        files = {
            'speaker_wav': (os.path.basename(SPEAKER_WAV_PATH), audio_file, 'audio/wav')
        }
        response = requests.post(API_URL, data=data, files=files)
        
    # ... rest of the response handling ...
    # (If the server is still running in the other terminal)
    
except requests.exceptions.ConnectionError:
    # ... connection error message ...
    pass
