import streamlit as st
import os
import time
import torch
import librosa
import matplotlib.pyplot as plt
import pandas as pd
from models.wav2vec import processor, model
from models.generator import rectify_statement
from data.dataFetcher import DatabaseManager

# Set up directory and ensure it exists
save_dir = "./audio_files"
os.makedirs(save_dir, exist_ok=True)

st.sidebar.title("NaturalQL")
st.sidebar.info(
    "Welcome! This app lets you simply give an audio input in natural language to fetch live data from database. "
    "You can also visualize the data using different chart types. "
)

st.markdown(
    """
    <h1 style='color:#4F8BF9;'>🎙️ NaturalQL: Speech to SQL using Effective Context Injection</h1>
    """,
    unsafe_allow_html=True
)

# Step 1: Record audio
st.markdown("#### 1️⃣ Record your audio")
audio_file = st.audio_input("Click the button below and speak into your microphone.")

# Step 2: Save and playback
if audio_file:
    filename = f"audio_{int(time.time())}.wav"
    save_path = os.path.join(save_dir, filename)
    with open(save_path, "wb") as f:
        f.write(audio_file.getbuffer().tobytes())

    st.success(f"✅ Audio recorded and saved as `{filename}` in `{save_dir}`.")
    st.audio(audio_file, format="audio/wav")
    st.download_button(
        label="⬇️ Download your recording",
        data=audio_file.getbuffer().tobytes(),
        file_name=filename,
        mime="audio/wav"
    )
    audio_file = ''
    # Only process if new audio
    if st.session_state.get('last_audio') != filename:
        # Expensive processing only here!
        dbEngine = DatabaseManager()
        audio, rate = librosa.load(save_path, sr=16000)
        input_values = processor(audio, return_tensors="pt").input_values
        with torch.no_grad():
            logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.decode(predicted_ids[0])
        dbSchema = dbEngine.fetch_schema()
        sql = rectify_statement(dbSchema, transcription)
        df = dbEngine.fetch_data(sql)

        # Store in session state
        st.session_state['last_audio'] = filename
        st.session_state['transcription'] = transcription
        st.session_state['dbSchema'] = dbSchema
        st.session_state['sql'] = sql
        st.session_state['df'] = df

else:
    st.info("Press the record button above to start.")

# Use cached results (if available), else empty defaults
transcription = st.session_state.get('transcription', "")
dbSchema = st.session_state.get('dbSchema', "")
sql = st.session_state.get('sql', "")
df = st.session_state.get('df', pd.DataFrame())

# Show results if available
if not df.empty:
    st.markdown("#### 3️⃣ Transcription")
    st.code(transcription, language="python")
    st.markdown("#### 2️⃣ SQL Query")
    st.code(sql, language="sql")
    st.write(df)

    # Chart UI
    chart_type = st.selectbox("Select chart type", ["Bar Chart", "Line Chart", "Pie Chart"])
    x_axis = st.selectbox("Select X axis", options=df.columns, index=0)
    numeric_columns = df.select_dtypes(include='number').columns.tolist()
    y_axis = st.selectbox("Select Y axis", options=numeric_columns, index=0)

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
