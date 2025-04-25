# pyttsgen/__init__.py
__version__ = "0.1.1"

from .engine import generate_speech, generate_speech_base64
from .utils import setup_logger

class TTS:
    """
    TTS class for a simple, plug-and-play interface.
    
    Examples:
      >>> from pyttsgen import TTS
      >>> tts = TTS()
      >>> tts.speak_to_file("Hello world!", "hello.mp3")
      >>> audio_bytes = tts.speak_to_bytes("I work in any framework!")
      >>> audio_base64 = tts.speak_to_base64("Send me to the browser!")
    """
    def __init__(self, voice: str = None):
        from .config import DEFAULT_VOICE
        self.voice = voice if voice else DEFAULT_VOICE
        self.logger = setup_logger()

    def speak_to_file(self, text: str, output_path: str) -> None:
        """Generate speech and save the output to a file."""
        self.logger.info("Generating speech to file: %s", output_path)
        generate_speech(text, self.voice, output_path)

    def speak_to_bytes(self, text: str) -> bytes:
        """Generate speech and return the output as bytes."""
        self.logger.info("Generating speech to bytes.")
        return generate_speech(text, self.voice)
    
    def speak_to_base64(self, text: str) -> str:
        """Generate speech and return the output as a base64 encoded string."""
        self.logger.info("Generating speech to base64 string.")
        return generate_speech_base64(text, self.voice)

    def speak_batch_to_files(self, texts: list, output_folder: str = "./") -> None:
        """
        Generate speech for a batch of texts, saving each output in the specified folder.
        
        :param texts: List of input text strings.
        :param output_folder: Folder where audio files will be saved.
        """
        import os
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        for i, text in enumerate(texts, start=1):
            output_path = os.path.join(output_folder, f"output_{i}.mp3")
            self.logger.info("Generating file: %s", output_path)
            generate_speech(text, self.voice, output_path)
