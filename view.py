import streamlit as st
import os
import time
import torch
import librosa
from models.wav2vec import tokenizer, model
import speech_recognition as sr
from models.schemaFetch import fetchSchema
from models.generator import rectify_statement
from data.dataFetcher import fetchData
import matplotlib.pyplot as plt
import pandas as pd

r = sr.Recognizer()
# Set up directory and ensure it exists
save_dir = "./audio_files"
os.makedirs(save_dir, exist_ok=True)

# Sidebar for navigation and instructions
st.sidebar.title("🎤 Audio Recorder")
st.sidebar.info(
    "Welcome! This app lets you record your voice and save it as a WAV file. "
    "Your recordings will be stored in the audio_files folder for later use."
)

# Main title and subtitle
st.markdown(
    """
    <h1 style='color:#4F8BF9;'>🎙️ Interactive Audio Recorder</h1>
    <p style='font-size:18px;'>Easily record, play back, and save your audio for further processing.</p>
    """,
    unsafe_allow_html=True
)

df = pd.DataFrame()
# Step 1: Record audio
st.markdown("#### 1️⃣ Record your audio")
audio_file = st.audio_input("Click the button below and speak into your microphone.")
# Step 2: Save and playback
if audio_file:
    # Create a unique filename using timestamp
    filename = f"audio_{int(time.time())}.wav"
    save_path = os.path.join(save_dir, filename)
    with open(save_path, "wb") as f:
        f.write(audio_file.getbuffer().tobytes())
    
    # Success message and playback
    st.success(f"✅ Audio recorded and saved as `{filename}` in `{save_dir}`.")
    st.audio(audio_file, format="audio/wav")
    
    # Download button for convenience
    st.download_button(
        label="⬇️ Download your recording",
        data=audio_file.getbuffer().tobytes(),
        file_name=filename,
        mime="audio/wav"
    )

    if 'last_audio' not in st.session_state or st.session_state.last_audio != filename:
        # Wav2Vec Approach
        audio, rate = librosa.load(save_path, sr=16000)
        input_values = tokenizer(audio, return_tensors="pt").input_values
        with torch.no_grad():
            logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = tokenizer.decode(predicted_ids[0])
        dbSchema = fetchSchema()
        sql = rectify_statement(dbSchema, transcription)
        df = fetchData(sql)

        # Store results in session_state
        st.session_state.last_audio = filename
        st.session_state.transcription = transcription
        st.session_state.sql = sql
        st.session_state.df = df

    # Use cached results from session_state
    transcription = st.session_state.transcription
    sql = st.session_state.sql
    df = st.session_state.df
    
    # try:
    #     with sr.AudioFile(save_path) as source:
    #         audio = r.record(source)
    #     text = r.recognize_google(audio)
    #     print("Transcription:", text)
    # except sr.UnknownValueError:
    #     print("Could not understand audio")
    # except sr.RequestError as e:
    #     print(f"Could not request results; {e}")

    
    st.markdown("#### 3️⃣ Transcription")
    st.code(transcription, language="python")
    st.markdown("#### 2️⃣ SQL Query")
    st.code(sql, language="sql")
    st.write(df)
else:
    st.info("Press the record button above to start.")

columns = df.columns.tolist()
chart_type = st.selectbox("Select chart type", ["Bar Chart", "Line Chart", "Pie Chart"])

# Axis selection
x_axis = st.selectbox("Select X axis", options=df.columns, index=0)
numeric_columns = df.select_dtypes(include='number').columns.tolist()
y_axis = st.selectbox("Select Y axis", options=numeric_columns, index=0)

# Show only the selected chart
if chart_type == "Bar Chart":
    st.markdown("### Bar Chart")
    st.bar_chart(df, x=x_axis, y=y_axis)

elif chart_type == "Line Chart":
    st.markdown("### Line Chart")
    st.line_chart(df, x=x_axis, y=y_axis)

elif chart_type == "Pie Chart":
    st.markdown("### Pie Chart")
    fig, ax = plt.subplots()
    ax.pie(df[y_axis], labels=df[x_axis], autopct='%1.1f%%')
    ax.axis("equal")
    st.pyplot(fig)

# Step 3: Show saved files
with st.expander("📁 Show saved recordings"):
    files = sorted(os.listdir(save_dir))
    if files:
        for f in files:
            st.markdown(f"- `{f}`")
    else:
        st.write("No recordings saved yet.")

