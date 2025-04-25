# pyttsgen/engine.py

import asyncio
import base64
import os
import tempfile
from io import BytesIO

import edge_tts
from .config import DEFAULT_VOICE

async def _generate_speech_async(text: str, voice: str, output_path: str = None) -> bytes:
    """
    Asynchronously generate speech audio using Edge TTS.
    When an output_path is provided, audio is written there.
    Otherwise, a temporary file is used, then removed after reading.
    """
    communicate = edge_tts.Communicate(text, voice)
    
    if output_path:
        # Generate directly to specified file
        await communicate.save(output_path)
        with open(output_path, "rb") as f:
            audio_bytes = f.read()
    else:
        # Use a temporary file if no output_path is provided.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            temp_filename = tmp_file.name
        try:
            await communicate.save(temp_filename)
            with open(temp_filename, "rb") as f:
                audio_bytes = f.read()
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
    
    return audio_bytes

def generate_speech(text: str, voice: str = DEFAULT_VOICE, output_path: str = None) -> bytes:
    """
    Synchronously generate speech from text.
    
    :param text: Input text to synthesize.
    :param voice: Voice identifier; defaults to DEFAULT_VOICE.
    :param output_path: Optional file path to save audio.
    :return: Audio content as bytes.
    """
    return asyncio.run(_generate_speech_async(text, voice, output_path))

def generate_speech_base64(text: str, voice: str = DEFAULT_VOICE) -> str:
    """
    Generate speech and return the audio as a base64 encoded string.
    
    :param text: Input text to synthesize.
    :param voice: Voice identifier.
    :return: Base64 encoded audio string.
    """
    audio_bytes = generate_speech(text, voice)
    return base64.b64encode(audio_bytes).decode('utf-8')
