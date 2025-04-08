import streamlit as st
import speech_recognition as sr
import language_tool_python
import tempfile
import os

# Set page configuration
st.set_page_config(page_title="Grammar Scoring from Speech", layout="wide")

# Sidebar
with st.sidebar:
    st.title("🎙️ Grammar Scorer")
    st.markdown("""
    Upload a WAV audio file and let the app:
    - Transcribe your speech
    - Check grammar
    - Provide suggestions
    - Generate a grammar score
    - Display corrected text
    """)
    uploaded_file = st.file_uploader("Upload your audio file", type=["wav"])
    st.markdown("---")
    st.markdown("Developed with ❤️ using Streamlit")

# Main area
st.title("🗣️ Grammar Scoring System for Spoken Audios")
st.markdown("""
This tool helps you evaluate how grammatically correct your speech is. Powered by:
- Google Speech Recognition
- LanguageTool Grammar Engine
""")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(uploaded_file.read())
        audio_path = tmp_file.name

    # Transcribe audio
    st.subheader("📜 Step 1: Transcribing Audio")
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)
            text = r.recognize_google(audio)
            st.success("✅ Audio Transcribed Successfully")
            st.text_area("📝 Transcribed Text", text, height=150)

            # Grammar checking
            st.subheader("🔍 Step 2: Grammar Check")
            tool = language_tool_python.LanguageTool('en-US')
            matches = tool.check(text)

            col1, col2 = st.columns([1, 2])
            col1.metric(label="📉 Grammar Issues", value=f"{len(matches)}")
            total_words = len(text.split())
            error_count = len(matches)
            grammar_score = max(0, 100 - (error_count / max(total_words, 1) * 100))
            col2.metric(label="📊 Grammar Score", value=f"{grammar_score:.2f}/100")

            st.markdown("---")
            st.subheader("📌 Issues & Suggestions")
            if matches:
                for i, match in enumerate(matches, 1):
                    with st.expander(f"Issue #{i}: {match.message}"):
                        st.write(f"**Suggestion:** {', '.join(match.replacements)}")
                        st.write(f"**Sentence:** {match.context}")
            else:
                st.success("No grammar issues found! 🎉")

            # Corrected text
            st.markdown("---")
            corrected = tool.correct(text)
            st.subheader("✅ Step 3: Corrected Text")
            st.text_area("🧠 Improved Version", corrected, height=150)

    except Exception as e:
        st.error(f"❌ Error processing audio: {e}")
    finally:
        os.remove(audio_path)
else:
    st.info("⬅️ Please upload an audio file from the sidebar to begin.")