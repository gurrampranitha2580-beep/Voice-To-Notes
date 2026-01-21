import streamlit as st
import speech_recognition as sr
import tempfile
import os

st.title("🎓 Lecture Voice-to-Notes Generator")
st.write("Upload a WAV audio file to generate lecture notes")

audio_file = st.file_uploader("Upload WAV audio", type=["wav"])

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        temp_path = tmp.name

    with sr.AudioFile(temp_path) as source:
        audio_data = recognizer.record(source)

    os.remove(temp_path)

    text = recognizer.recognize_google(audio_data)
    return text

if audio_file is not None:
    st.audio(audio_file)

    with st.spinner("Transcribing lecture..."):
        try:
            transcript = transcribe_audio(audio_file)
            st.subheader("📝 Transcription")
            st.write(transcript)
        except Exception as e:
            st.error("Speech recognition failed. Please use clear WAV audio.")
