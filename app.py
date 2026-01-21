import streamlit as st
import speech_recognition as sr
import tempfile
import os

# --- Page configuration ---
st.set_page_config(
    page_title="Lecture Voice-to-Notes",
    page_icon="📝",
    layout="centered"
)

# --- Title & description ---
st.markdown("<h1 style='text-align: center; color: #4B0082;'>🎓 Lecture Voice-to-Notes Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6A5ACD;'>Upload your lecture audio (WAV) and get instant notes!</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Instructions ---
st.markdown("**Instructions:**")
st.markdown("""
1. Prepare your lecture audio in **WAV format**  
2. Click the **Upload** button below  
3. Wait a few seconds for transcription to appear  
4. Copy or save your notes for studying!
""")

# --- File uploader ---
audio_file = st.file_uploader("Upload your lecture audio (WAV only) 🎤", type=["wav"])

# --- Function to transcribe ---
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

# --- Simple summary function ---
def summarize_text(text, max_sentences=5):
    sentences = text.split('. ')
    summary = '. '.join(sentences[:max_sentences])
    return summary

# --- Run transcription + summary + quiz + flashcards ---
if audio_file is not None:
    st.audio(audio_file)
    with st.spinner("Transcribing your lecture... ⏳"):
        try:
            transcript = transcribe_audio(audio_file)

            # Transcription
            st.subheader("📝 Transcription")
            st.write(transcript)

            # Summary
            st.subheader("📌 Summary")
            summary = summarize_text(transcript)
            st.write(summary)

            # Quiz Questions
            st.subheader("❓ Quiz Questions")
            quiz_sentences = transcript.split('. ')
            for i, q in enumerate(quiz_sentences[:3], 1):
                st.write(f"Q{i}: {q.strip()}?")

            # Flashcards
            st.subheader("💡 Flashcards")
            for i, q in enumerate(quiz_sentences[:3], 1):
                st.write(f"Front (Q{i}): {q.strip()}?")
                st.write(f"Back (A{i}): {q.strip()}")

        except Exception as e:
            st.error("Speech recognition failed. Please use clear WAV audio.")
