# pyttsgen/web.py

import streamlit as st
from .engine import generate_speech

def launch_ui():
    """
    Launch a Streamlit UI to demonstrate the TTS functionality.
    This is for demo purposes only and doesn't affect core library usage.
    """
    st.title("pyttsgen: Text-to-Speech Demo")
    st.write("Enter your text and select a voice to generate audio.")
    
    text = st.text_area("Enter text:", height=150)
    voice = st.text_input("Voice Identifier:", value="en-US-AriaNeural")
    
    if st.button("Generate Audio"):
        if not text.strip():
            st.error("Please enter some text!")
        else:
            output_file = "output.mp3"  # temporary file for demo usage
            st.spinner("Generating audio...")
            audio_bytes = generate_speech(text, voice, output_file)
            st.success("Audio generated!")
            st.audio(audio_bytes, format="audio/mp3")
            st.download_button("Download Audio", audio_bytes,
                               file_name=output_file, mime="audio/mp3")

if __name__ == "__main__":
    launch_ui()
