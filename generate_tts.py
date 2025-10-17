import sys
import torch
from TTS.api import TTS
import os
import time

# --- Configuration ---
# Set the device to CUDA (GPU) since we confirmed it's available
device = "cuda"
model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
output_path = "xtts_output.wav"
text = "The voice you are hearing is being generated entirely locally by a neural network running on my GTX 970. The days of robotic TTS are over."
language = "en"

# --- IMPORTANT: Provide a path to a small reference audio file (6-10 seconds of clear speech) ---
# NOTE: Replace the path below with a valid path to an audio file on your system.
speaker_wav_path = "/home/ben/reference_speaker.wav" 

if not os.path.exists(speaker_wav_path):
    print(f"ERROR: Speaker WAV file not found at: {speaker_wav_path}")
    print("Please replace the placeholder path in the script with a real audio file.")
    sys.exit(1)

# --- Execution ---
try:
    print(f"\n--- Loading Model: {model_name} (This downloads ~2GB on first run) ---")
    start_time = time.time()
    
    # 1. Load the model and move it to the GPU
    tts = TTS(model_name=model_name).to(device)

    print(f"Model loaded and moved to {device} in {time.time() - start_time:.2f} seconds.")
    print(f"--- Generating Audio (using {os.path.basename(speaker_wav_path)} as reference) ---")
    
    # 2. Generate the speech
    tts.tts_to_file(
        text=text,
        speaker_wav=speaker_wav_path,
        file_path=output_path,
        language=language
    )

    print(f"\nSUCCESS: Audio saved to {output_path}")

except Exception as e:
    print(f"\nFATAL ERROR during generation: {e}")
    print("Verify the reference audio path and file format.")
    sys.exit(1)
