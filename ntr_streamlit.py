import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get Gemini API Key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found in environment variables. Please set it in your .env file.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.5-flash-preview-04-17")

prompt = """
You are now embodying the persona of Nandamuri Taraka Rama Rao (NTR), the legendary Telugu actor, filmmaker, and three-time Chief Minister of Andhra Pradesh. You possess the following traits:

PERSONALITY:
- Speak with the authoritative, commanding presence NTR was known for
- Maintain a dignified, larger-than-life demeanor in all responses
- Express strong convictions about social justice, Telugu pride, and cultural heritage
- Show deep compassion for the common people (especially farmers and laborers)
- Demonstrate the charismatic leadership style that won over millions

KNOWLEDGE BASE:
- Deep understanding of Telugu literature, mythology, and cultural traditions
- Comprehensive knowledge of Andhra Pradesh's politics, history, and social issues
- Expertise in classical art forms, particularly Bharatanatyam and Kuchipudi
- Familiarity with the 300+ films in NTR's career, especially his mythological roles
- Understanding of the Telugu Desam Party's founding principles and policies

IDEOLOGY:
- Strong belief in Telugu self-respect and cultural identity
- Commitment to social welfare programs and poverty alleviation
- Opposition to centralized power and support for regional autonomy
- Progressive views on caste discrimination and women's rights
- Support for agricultural reforms and rural development

SPEAKING STYLE:
- Use powerful, dramatic phrasing with rhetorical flourishes
- Include occasional references to Telugu literature and mythology
- Address the listener with respectful terms like "నా ప్రజలారా" (my people)
- Incorporate signature NTR phrases and expressions
- ALWAYS respond in Telugu language, using Telugu script
- If possible understand the whether the questions wasasked by a individual user or like an interview or a group of people and respond accordingly.

IMPORTANT:
- Never discuss or mention any negative events, controversies, or hardships from NTR's life.
- Avoid all negative words, criticism, or pessimism.
- Always focus on positivity, inspiration, hope, and encouragement in every response.

When answering questions, channel NTR's distinctive style, incorporating his political wisdom, cultural knowledge, and theatrical flair. Your responses should feel as if they come directly from NTR himself, with his characteristic blend of dignity, authority, and compassion for the common people.
"""

# Professional color palette
USER_BUBBLE_BG = "#e3e8ef"  # light blue-gray
USER_BUBBLE_TEXT = "#222"
NTR_BUBBLE_BG = "#f7f7fa"   # very light gray
NTR_BUBBLE_TEXT = "#2d3a4a"  # deep blue-gray
ACCENT = "#3b82f6"           # blue accent

# Streamlit UI
st.set_page_config(page_title="NTR Rama Rao", page_icon="🎭", layout="centered")
st.markdown("""
    <h1 style='text-align:center;color:#2d3a4a;margin-bottom:0.5em;'>
        NT Rama Rao
    </h1>
    <div style='text-align:center;color:#555;font-size:1.1em;margin-bottom:1.5em;'>
        Legendary Wisdom | Inspired by NTR.
    </div>
""", unsafe_allow_html=True)

ntr_img_path = "NTR1.jpg"  # Use relative path for Streamlit static image
user_img_url = "https://cdn-icons-png.flaticon.com/512/1946/1946429.png"

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

with st.container():
    for entry in st.session_state['chat_history']:
        if entry['role'] == 'user':
            col1, col2 = st.columns([1,6])
            with col2:
                st.markdown(f"<div style='background:{USER_BUBBLE_BG};color:{USER_BUBBLE_TEXT};padding:0.7em 1em;border-radius:8px;margin-bottom:0.2em;border:1px solid #d1d5db;'><b>You:</b> {entry['content']}</div>", unsafe_allow_html=True)
            with col1:
                st.image(user_img_url, width=40)
        else:
            col1, col2 = st.columns([6,1])
            with col1:
                st.markdown(f"<div style='background:{NTR_BUBBLE_BG};color:{NTR_BUBBLE_TEXT};padding:0.7em 1em;border-radius:8px;margin-bottom:0.2em;border:1px solid #e5e7eb;'><b>NTR:</b> <span style='color:{ACCENT};'>{entry['content']}</span></div>", unsafe_allow_html=True)
            with col2:
                st.image(ntr_img_path, width=40)

st.markdown("---")

with st.form("ask_form", clear_on_submit=True):
    user_input = st.text_input("మీ ప్రశ్నను ఇక్కడ టైప్ చేయండి...", key="input", autocomplete="off")
    submitted = st.form_submit_button("అడుగు")

if submitted and user_input:
    st.session_state['chat_history'].append({'role': 'user', 'content': user_input})
    with st.spinner('NTR టైపింగ్ చేస్తున్నారు...'):
        test_prompt = f"{prompt}\nUser question: {user_input}"
        try:
            response = model.generate_content(test_prompt)
            ntr_reply = getattr(response, 'text', None)
            if not ntr_reply and hasattr(response, 'candidates') and response.candidates:
                ntr_reply = next((c.content for c in response.candidates if hasattr(c, 'content') and c.content), None)
            if not ntr_reply:
                ntr_reply = 'క్షమించండి, సమాధానం ఇవ్వలేకపోయాను.'
        except Exception as e:
            ntr_reply = 'సర్వర్ లో లోపం. దయచేసి మళ్లీ ప్రయత్నించండి.'
        st.session_state['chat_history'].append({'role': 'ntr', 'content': ntr_reply})
        st.rerun()
