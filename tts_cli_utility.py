import argparse
import os
import sys
import torch
from TTS.api import TTS

# --- Configuration Constants ---
# Default model: XTTS-v2 (Requires speaker_wav)
DEFAULT_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"
# Default speaker file: Use the clean, local file you generated
DEFAULT_SPEAKER_WAV = "/home/ben/safe_reference.wav" 
DEFAULT_LANGUAGE = "en"
DEFAULT_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def generate_tts_audio(input_file_path, speaker_wav_path, output_file_path, language, device):
    """Loads the XTTS model and synthesizes audio from a text file."""
    
    # 1. Path and File Validation
    if not os.path.exists(input_file_path):
        print(f"ERROR: Input text file not found at: {input_file_path}")
        sys.exit(1)
    if not os.path.exists(speaker_wav_path):
        print(f"ERROR: Speaker WAV file not found at: {speaker_wav_path}")
        print("Please ensure your reference audio is available.")
        sys.exit(1)

    # 2. Load Text Content
    try:
        # Use simple read (Python 3 defaults to UTF-8)
        with open(input_file_path, 'r', encoding='utf-8') as f:
            article_text = f.read()
    except Exception as e:
        print(f"ERROR: Could not read input file: {e}")
        sys.exit(1)

    if not article_text.strip():
        print(f"ERROR: Input file '{input_file_path}' is empty.")
        sys.exit(1)

    # 3. Load and Run TTS Model
    try:
        print(f"Loading XTTS model onto device: {device}...")
        # Load the model and move it to the GPU/CPU
        tts = TTS(model_name=DEFAULT_MODEL).to(device)

        print(f"Generating audio for {len(article_text)} characters...")
        tts.tts_to_file(
            text=article_text,
            speaker_wav=speaker_wav_path,
            file_path=output_file_path,
            language=language,
            split_sentences=True 
        )
        print("\n" + "="*50)
        print(f"✅ SUCCESS! Audio saved to: {output_file_path}")
        print("="*50)

    except Exception as e:
        print(f"\nFATAL RUNTIME ERROR during generation: {e}")
        print("Model execution failed. Check CUDA status or VRAM availability.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Run Coqui XTTS-v2 (GPU Accelerated) to synthesize audio from a text file.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # --- Required Argument ---
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input text file (.txt) to be read."
    )
    
    # --- Optional Arguments (with ENV defaults) ---
    parser.add_argument(
        "-s", "--speaker",
        type=str,
        default=os.environ.get('TTS_SPEAKER_WAV', DEFAULT_SPEAKER_WAV),
        help=f"Path to the speaker WAV file for voice cloning (XTTS only).\nDefault (or TTS_SPEAKER_WAV ENV): {DEFAULT_SPEAKER_WAV}"
    )
    parser.add_argument(
        "-l", "--language",
        type=str,
        default=os.environ.get('TTS_LANGUAGE', DEFAULT_LANGUAGE),
        help=f"Language code (e.g., 'en', 'es', 'fr').\nDefault (or TTS_LANGUAGE ENV): {DEFAULT_LANGUAGE}"
    )
    parser.add_argument(
        "-d", "--device",
        type=str,
        default=os.environ.get('TTS_DEVICE', DEFAULT_DEVICE),
        help=f"Compute device ('cuda' or 'cpu').\nDefault (or TTS_DEVICE ENV): {DEFAULT_DEVICE}"
    )

    args = parser.parse_args()

    # --- Determine Output Path (Same folder, new suffix) ---
    input_dir = os.path.dirname(args.input_file)
    input_filename_base = os.path.splitext(os.path.basename(args.input_file))[0]
    output_file_path = os.path.join(input_dir, f"{input_filename_base}.wav")

    # If input_dir is empty (file is in CWD), ensure output is CWD too.
    if not input_dir:
        output_file_path = f"{input_filename_base}.wav"

    # --- Call the synthesis function ---
    generate_tts_audio(
        input_file_path=args.input_file,
        speaker_wav_path=args.speaker,
        output_file_path=output_file_path,
        language=args.language,
        device=args.device
    )

if __name__ == "__main__":
    # Ensure (tts_venv) is active before running
    if 'tts_venv' not in os.environ.get('VIRTUAL_ENV', ''):
        print("Warning: Virtual environment not detected. Ensure 'source tts_venv/bin/activate' has been run.")
        print("Using environment defaults...")
    
    # Run the main utility
    main()
