import streamlit as st
import pandas as pd
import plotly.express as px
import random
import openai
import os
from tempfile import NamedTemporaryFile

# Set up page
st.set_page_config(page_title="Lead Funnel Intelligence Dashboard", layout="wide")
st.title("🤖 AI-Powered Lead Funnel Intelligence Report")

# Dashboard intro text
st.markdown("Upload a CSV lead file and/or demo call audio to generate actionable insights, enriched scores, and personalized follow-up strategies — powered by AI.")

# ========== Audio Transcription Section ==========
st.header("🎙️ AI Call Transcription")
st.write("Upload a demo call audio file (.mp3 or .wav) to generate a transcript you can use to personalize follow-ups.")

audio_file = st.file_uploader("Upload audio file", type=["mp3", "wav"], key="audio_uploader")

if audio_file:
    openai.api_key = st.secrets["openai_api_key"] if "openai_api_key" in st.secrets else os.getenv("OPENAI_API_KEY")

    with NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(audio_file.read())
        tmp_path = tmp_file.name

    with st.spinner("Transcribing with Whisper..."):
        try:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=open(tmp_path, "rb"),
                response_format="text"
            )
            st.subheader("📄 Transcribed Call")
            st.text_area("Transcript", transcript, height=300)
        except Exception as e:
            st.error(f"Transcription failed: {e}")

st.write("✅ Transcript section loaded")

# ========== CSV Lead File Upload & Analysis ==========
uploaded_file = st.file_uploader("Upload your CSV lead file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file, header=1)
    df.columns = df.columns.str.strip()

    st.subheader("📄 Uploaded Lead Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    # Lead Segmentation
    st.header("📊 Lead Segmentation")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("By Description")
        top_descriptions = df['description'].value_counts().nlargest(10)
        fig1 = px.bar(top_descriptions, title="Top Startup Descriptions", labels={'value': 'Count', 'index': 'Description'})
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("By Location")
        top_locations = df['location'].value_counts().nlargest(10)
        fig2 = px.bar(top_locations, title="Top Locations", labels={'value': 'Count', 'index': 'Location'})
        st.plotly_chart(fig2, use_container_width=True)

    # Conversion Readiness Score
    st.header("🔥 Conversion Readiness Score")
    def score_lead(row):
        score = 0
        if isinstance(row['description'], str) and 'ai' in row['description'].lower():
            score += 50
        return min(score, 100)

    df['readiness_score'] = df.apply(score_lead, axis=1)
    st.write("### Top Leads by Readiness Score")
    st.dataframe(df[['startupName', 'readiness_score']].sort_values(by='readiness_score', ascending=False), use_container_width=True)
    fig4 = px.histogram(df, x='readiness_score', nbins=10, title="Readiness Score Distribution")
    st.plotly_chart(fig4, use_container_width=True)

    # Smart Follow-Up Schedule
    st.header("📆 Smart Follow-Up Schedule")
    follow_up_choices = ['Follow up today', 'Follow up next week', 'Wait']
    df['follow_up'] = [random.choice(follow_up_choices) for _ in range(len(df))]
    for choice in follow_up_choices:
        st.subheader(choice)
        st.dataframe(df[df['follow_up'] == choice][['startupName', 'contact1', 'readiness_score']], use_container_width=True)

    # Download enriched data
    st.download_button("⬇️ Download Scored Leads as CSV", data=df.to_csv(index=False), file_name="enhanced_leads.csv", mime="text/csv")
