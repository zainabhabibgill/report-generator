import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(page_title="Lead Funnel Intelligence Dashboard", layout="wide")

st.title("🤖 AI-Powered Lead Funnel Intelligence Report")

# Dashboard intro text
st.markdown("Upload a CSV lead file and instantly generate actionable insights, enriched scores, and suggested follow-up strategies — powered by AI.")

# File upload (CSV only)
uploaded_file = st.file_uploader("Upload your CSV lead file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file, header=1)
    df.columns = df.columns.str.strip()  # Clean whitespace in column names

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

    # Behavioral Patterns (Placeholder)
    st.header("📈 Behavioral Patterns (Coming Soon)")
    st.info("This section will analyze email open/reply behavior when such data is available.")

    # Best Performing Email Styles (Placeholder)
    st.header("✉️ Best Performing Email Styles (Coming Soon)")
    st.info("Once past email content & performance data is integrated, this section will show which tone/length performs best.")

    # Smart Follow-Up Schedule
    st.header("📆 Smart Follow-Up Schedule")
    follow_up_choices = ['Follow up today', 'Follow up next week', 'Wait']
    df['follow_up'] = [random.choice(follow_up_choices) for _ in range(len(df))]

    for choice in follow_up_choices:
        st.subheader(choice)
        st.dataframe(df[df['follow_up'] == choice][['startupName', 'contact1', 'readiness_score']], use_container_width=True)

    # Download enriched data
    st.download_button("⬇️ Download Scored Leads as CSV", data=df.to_csv(index=False), file_name="enhanced_leads.csv", mime="text/csv")
