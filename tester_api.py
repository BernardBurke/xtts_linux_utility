import requests
import os
import sys

# --- Configuration ---
# NOTE: Ensure your server is running on this address/port
API_URL = "http://127.0.0.1:5002/api/tts" 
TEXT_TO_SYNTHESIZE = "This message was generated using a local API server on a dedicated Linux machine."
OUTPUT_WAV_PATH = "api_output.wav"

# --- IMPORTANT: Configure Your File Path ---
# Replace this path with the ABSOLUTE path you confirmed works via ls
SPEAKER_WAV_PATH = "/tmp/safe_reference.wav" 

# --- Data Preparation ---
data = {
    "text": TEXT_TO_SYNTHESIZE,
    "language": "en" 
}

# --- Request Execution ---
try:
    print(f"Sending request for: '{TEXT_TO_SYNTHESIZE[:40]}...'")
    
    # Check if file exists on the client side before attempting to open
    if not os.path.exists(SPEAKER_WAV_PATH):
        print(f"FATAL CLIENT ERROR: Reference file not found at {SPEAKER_WAV_PATH}")
        sys.exit(1)

    # Use 'with open' to handle the file safely and ensure it closes
    with open(SPEAKER_WAV_PATH, 'rb') as audio_file:
        
        # This is the corrected file structure, using os.path.basename() for the filename
        files = {
            'speaker_wav': (os.path.basename(SPEAKER_WAV_PATH), audio_file, 'audio/wav')
        }
        
        # Send the POST request to the running server
        response = requests.post(API_URL, data=data, files=files)
    
    # --- Response Handling ---
    if response.status_code == 200:
        with open(OUTPUT_WAV_PATH, 'wb') as f:
            f.write(response.content)
        print(f"\nSUCCESS: Audio generated via API and saved to {OUTPUT_WAV_PATH}")
    else:
        print(f"\nERROR: API call failed with status code {response.status_code}")
        print(f"Server response: {response.text[:200]}...") # Print a snippet of the stack trace
        print("\nPossible Causes: The server is failing to read the audio encoding or the text is too long.")

except requests.exceptions.ConnectionError:
    print("\nERROR: Could not connect to the TTS server.")
    print("Ensure 'tts-server --model_name ... --use_cuda' is running on port 5002.")
