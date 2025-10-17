import requests

# NOTE: The server must be running in the background for this script to work!

API_URL = "http://127.0.0.1:5002/api/tts"
TEXT_TO_SYNTHESIZE = "This message was generated using a local API server on a dedicated Linux machine."
SPEAKER_WAV_PATH = "/home/ben/reference_speaker.wav"  # IMPORTANT: Use your actual reference file path
OUTPUT_WAV_PATH = "/home/ben/api_output.wav"

data = {
    "text": TEXT_TO_SYNTHESIZE,
    "language": "en" 
}

files = {
    'speaker_wav': (SPEAKER_WAV_PATH, open(SPEAKER_WAV_PATH, 'rb'), 'audio/wav')
}

try:
    print(f"Sending request for: '{TEXT_TO_SYNTHESIZE[:40]}...'")
    response = requests.post(API_URL, data=data, files=files)
    
    if response.status_code == 200:
        with open(OUTPUT_WAV_PATH, 'wb') as f:
            f.write(response.content)
        print(f"\nSUCCESS: Audio generated via API and saved to {OUTPUT_WAV_PATH}")
    else:
        print(f"\nERROR: API call failed with status code {response.status_code}")
        print(f"Server response: {response.text}")

except requests.exceptions.ConnectionError:
    print("\nERROR: Could not connect to the TTS server.")
    print("Please ensure 'tts-server' is running in the other terminal session and is not blocked by a firewall.")
