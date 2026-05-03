import streamlit as st
import requests
from ingest import process_book
from report_analyzer import extract_text_from_pdf  # Naya module import kiya

# API Key fetch karna
API_KEY = st.secrets["GEMINI_API_KEY"]

# RAG ke liye book load karna
try:
    medical_book_text = process_book() 
except Exception as e:
    medical_book_text = "Standard cardiology principles apply."

st.set_page_config(page_title="CardiAI | Medical AI", page_icon="🩺", layout="centered")

# UI Header
st.markdown("""
    <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; border-bottom: 4px solid #cc0000; margin-bottom: 25px;">
        <h1 style="color: #cc0000; text-align: center; margin: 0;">🧑‍⚕️ CardiAI: Heart Care Assistant</h1>
        <p style="color: #555; text-align: center; margin-bottom: 2px;">Advanced Cardiology RAG AI | B.Tech CSE Major Project</p>
        <p style="text-align: center; color: #cc0000; font-weight: 600;">M.J.P. Rohilkhand University</p>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Streamlit Tabs: 1 Chat ke liye, 1 Report ke liye
# ------------------------------------------------------------------
tab1, tab2 = st.tabs(["💬 General Consultation", "📄 Analyze Medical Report"])

# --- TAB 1: General Chatbot (RAG based on Book) ---
with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        avatar = "user" if message["role"] == "user" else "assistant"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    user_input = st.chat_input("Ask about symptoms, prevention, or heart health...")

    if user_input:
        st.chat_message("user", avatar="user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        system_prompt = f"""
        You are an expert cardiologist AI. Reference Material: {medical_book_text}
        User Question: {user_input}
        Answer based on the reference material. Do NOT prescribe medicines.
        """
        
        with st.spinner("🧑‍⚕️ Consulting reference books..."):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
                response = requests.post(url, headers={'Content-Type': 'application/json'}, json={"contents": [{"role": "user", "parts": [{"text": system_prompt}]}]})
                if response.status_code == 200:
                    bot_reply = response.json()['candidates'][0]['content']['parts'][0]['text']
                    with st.chat_message("assistant", avatar="assistant"):
                        st.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error("Error connecting to AI Server.")


# --- TAB 2: Medical Report Analyzer ---
with tab2:
    st.markdown("### 📄 Upload Lab Report / ECG Report (PDF)")
    st.info("Upload your medical report and the AI will simplify the findings and suggest precautions.")
    
    # Streamlit ka file uploader feature
    uploaded_file = st.file_uploader("Choose a PDF report", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Analyze Report 🔍"):
            with st.spinner("🧑‍⚕️ Analyzing Report Data..."):
                # Naye module se text nikalna
                report_text = extract_text_from_pdf(uploaded_file)
                
                # Report Analysis ke liye Strict System Prompt
                report_prompt = f"""
                You are a Cardiology AI Assistant. Analyze the following medical report:
                {report_text}
                
                Please provide:
                1. A simple summary of the findings (in layman's terms).
                2. Highlight any abnormal values (e.g., high cholesterol, blood pressure).
                3. General lifestyle and dietary recommendations based on the findings AND this medical book: {medical_book_text}.
                4. A STRICT WARNING: Tell the patient to consult a real doctor for diagnosis and medication. Do NOT prescribe any drugs.
                """
                
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
                    response = requests.post(url, headers={'Content-Type': 'application/json'}, json={"contents": [{"role": "user", "parts": [{"text": report_prompt}]}]})
                    
                    if response.status_code == 200:
                        analysis_reply = response.json()['candidates'][0]['content']['parts'][0]['text']
                        st.success("Analysis Complete!")
                        st.markdown(analysis_reply)
                    else:
                        st.error("Failed to analyze report via API.")
                except Exception as e:
                    st.error("Error processing report.")