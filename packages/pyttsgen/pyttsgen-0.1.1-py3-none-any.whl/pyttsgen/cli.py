# pyttsgen/cli.py

import argparse
from .config import VOICES, DEFAULT_VOICE
from .engine import generate_speech

def list_voices():
    """Print out available voices and their identifiers."""
    print("Available voices:")
    for name, identifier in VOICES.items():
        print(f"- {name}: {identifier}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate TTS audio from text using pyttsgen."
    )
    parser.add_argument("text", type=str, nargs="?", help="Input text to synthesize")
    parser.add_argument("--voice", type=str, default=DEFAULT_VOICE,
                        help="Voice to use (provide voice identifier)")
    parser.add_argument("--output", type=str, default="output.mp3",
                        help="Output file path for the audio")
    parser.add_argument("--list-voices", action="store_true",
                        help="List all available voices")
    args = parser.parse_args()

    if args.list_voices:
        list_voices()
        return

    if not args.text:
        print("Error: Please provide text for synthesis.")
        return

    generate_speech(args.text, args.voice, args.output)
    print("Audio generated and saved to", args.output)

if __name__ == "__main__":
    main()
