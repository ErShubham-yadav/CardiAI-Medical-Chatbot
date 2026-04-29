import streamlit as st
import requests

# Set page configurations (Must be the very first Streamlit command)
st.set_page_config(
    page_title="CardiAI | Medical Heart Disease Chatbot",
    page_icon="🩺",  # Attractive stethoscope icon for browser tab
    layout="centered",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------------
# Advanced Custom CSS for a Professional Medical UI
# ------------------------------------------------------------------
def local_css():
    st.markdown("""
        <style>
        /* General Font Styling - Modern & Professional */
        @import url('https://fonts.googleapis.com/css2?family=Segoe+UI&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
        }

        /* Styling for the Main stylized header */
        .medical-header {
            background-color: #f0f8ff; /* Light medical blue background */
            padding: 20px;
            border-radius: 10px;
            border-bottom: 4px solid #cc0000; /* Medical red accent line */
            margin-bottom: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .header-title {
            color: #cc0000; /* Red color for medical theme */
            font-size: 36px !important;
            font-weight: bold !important;
            text-align: center;
            margin: 0;
        }
        .header-sub-title {
            color: #555;
            text-align: center;
            font-size: 16px;
            margin-top: 5px;
        }

        /* Highlighting specific components */
        .stButton>button {
            color: white;
            background-color: #cc0000; /* Red for medical importance */
            border-radius: 10px;
            width: 100%;
        }
        .stChatInput>div {
            border-radius: 15px; /* Rounded corners for input */
        }

        /* Sidebar styling for professional appeal */
        .css-1634w34 {
            background-color: #fafafa;
        }
        .sidebar-heading {
            color: #2e8b57; /* Medical green for headings */
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 10px;
            margin-top: 20px;
        }
        .sidebar-text {
            font-size: 14px;
            color: #666;
            margin-bottom: 10px;
        }

        /* Spinner Styling - Making it attractive */
        .stSpinner>div>div {
            border-color: #cc0000 transparent transparent transparent;
        }
        </style>
    """, unsafe_allow_html=True)

# Apply the custom CSS
local_css()

# Insert your valid Google Gemini API key here
# Direct REST API requires direct key injection (local use only, never public Git)
# Streamlit backend se automatically API key fetch karega
API_KEY = st.secrets["GEMINI_API_KEY"] 

# ------------------------------------------------------------------
# Professional Sidebar Section
# ------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/heart-health.png", width=70) # Medical heart icon
    st.markdown('<p class="sidebar-heading">⚕️ Project Overview</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-text">CardiAI is an advanced heart care AI assistant designed to provide medical information regarding cardiovascular health.</p>', unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-heading">⚠️ Important Limitations</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-text">• This is an informational AI and NOT a substitute for professional medical advice.</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-text">• Do NOT share sensitive personal health data.</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-text">• Always consult a doctor for a medical emergency.</p>', unsafe_allow_html=True)
    
    # Add a "Start New Conversation" button (Simulates a refresh)
    if st.button("🔄 Start New Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

# ------------------------------------------------------------------
# Main UI - Stylized Header with Medical Branding
# ------------------------------------------------------------------
st.markdown("""
    <div class="medical-header">
        <h1 class="header-title">🧑‍⚕️ CardiAI: Heart Care Assistant</h1>
        <p class="header-sub-title"> Cardiology AI Information Hub | Engineered from Scratch to Provide Smart Cardiovascular Insights</p>
    </div>
""", unsafe_allow_html=True)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages from history on app rerun
for message in st.session_state.messages:
    # Use standard modern avatars: "user" for patient, "assistant" for bot
    avatar = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Accept user input from the stylized chat interface at the bottom
user_input = st.chat_input("Describe your concern or ask about heart health symptoms...")

if user_input:
    # Display user message in the chat container
    st.chat_message("user", avatar="user").markdown(user_input)
    # Add user message to the chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Strict system prompt to keep AI focused only on Cardiology and Prevention
    system_prompt = f"""
    You are an expert cardiologist AI. Answer questions related to heart disease, symptoms, prevention, and general cardiovascular health. 
    IMPORTANT LEGAL & MEDICAL INSTRUCTIONS:
    1. Only provide medical information, NOT diagnoses or prescriptions.
    2. Suggest generic lifestyle improvements (e.g., diet, exercise) for prevention.
    3. Mandatory Disclaimer: Poltiely but firmly state multiple times that the user must consult a qualified human doctor before making health decisions.
    4. Emergency Protocol: If a user describes severe symptoms (e.g., severe chest pain), instruct them to call emergency services immediately.
    
    User Question: {user_input}
    """
    
    # Custom stylized spinner with Doctor emoji and professional responding message
    with st.spinner("🧑‍⚕️ Doctor is responding... Analyzing your cardiovascular query."):
        try:
            # REST API endpoint for Google Gemini (gemini-flash-latest model for speed)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [{"role": "user", "parts": [{"text": system_prompt}]}]
            }
            
            # Send the REST POST request with a timeout for reliability
            response = requests.post(url, headers=headers, json=data, timeout=45)
            
            # Handling API responses
            if response.status_code == 200:
                result = response.json()
                bot_reply = result['candidates'][0]['content']['parts'][0]['text']
                
                # Display assistant response in the chat container using bot avatar
                with st.chat_message("assistant", avatar="assistant"):
                    st.markdown(bot_reply)
                # Add assistant response to the chat history
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
            elif response.status_code == 429:
                st.warning("⚠️ High request traffic detected on Google's Free Tier. Please wait 15 seconds before asking another medical question.")
            
            else:
                st.error(f"🩺 A network issue occurred (API Code {response.status_code}). Please try again shortly.")
                
        except Exception as e:
            # Catching local system/network errors
            st.error("🚨 System Error: Unable to complete your cardiology query.")