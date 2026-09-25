import streamlit as st
import math
from PIL import Image, ImageEnhance
import google.generativeai as genai

st.set_page_config(
    page_title="NijaAI - Gemini Edition", 
    page_icon="✦", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

GEMINI_API_KEY = "AQ_AbaRN6JTyKztLGrKvjVK3UhFWfpFccjHmjRtUxBoxZqrbezHow"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
# ------------------------------------------------------------------

# Styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e0e10;
        color: #f0f0f0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .header-box {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 10px;
    }
    .hero-box {
        text-align: center;
        margin: 15px 0 20px 0;
    }
    .sparkle-icon {
        font-size: 2.6rem;
        background: linear-gradient(45deg, #4285F4, #9B72CB, #D96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 500;
        color: #e5e7eb;
        margin-top: 2px;
    }
    .dev-by {
        color: #9ca3af;
        font-size: 0.85rem;
        margin-top: 4px;
    }
    </style>
    <div class="header-box">
        <div style="font-size: 1.15rem; font-weight: 500; color: #d1d5db;">
            Gemini Flash <span style="font-size: 0.7rem; color: #60a5fa;">●</span>
        </div>
        <div style="background-color: #d9532f; color: white; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-weight: bold;">
            S
        </div>
    </div>
    <div class="hero-box">
        <div class="sparkle-icon">✦</div>
        <div class="hero-title">Let’s jump in, Santhu</div>
        <div class="dev-by">Developed by Santhosh D</div>
    </div>
    """,
    unsafe_allow_html=True
)

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Home"

def set_tab(name):
    st.session_state.active_tab = name

# Drawer Buttons
with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🖼️ Photos", use_container_width=True):
            set_tab("Photos")
    with col2:
        if st.button("📷 Camera", use_container_width=True):
            set_tab("Camera")
    with col3:
        if st.button("✨ Avatar", use_container_width=True):
            set_tab("Avatar")

    st.divider()

    c1, c2 = st.columns([1, 4])
    with c1:
        if st.button("🎨 Images", use_container_width=True):
            set_tab("Photos")
    with c2:
        st.caption("ಫೋಟೋಗಳನ್ನು ಎಡಿಟ್ ಮಾಡಿ")

    c3, c4 = st.columns([1, 4])
    with c3:
        if st.button("📹 Videos", use_container_width=True):
            set_tab("Videos")
    with c4:
        st.caption("ವೀಡಿಯೊ ಕಲ್ಪನೆಗಳು ಮತ್ತು ಸ್ಕ್ರಿಪ್ಟ್")

    c5, c6 = st.columns([1, 4])
    with c5:
        if st.button("🎵 Music", use_container_width=True):
            set_tab("Music")
    with c6:
        st.caption("ಹಾಡು ಮತ್ತು ಆಡಿಯೋ ಐಡಿಯಾಗಳು")

    c7, c8 = st.columns([1, 4])
    with c7:
        if st.button("📝 Canvas", use_container_width=True):
            set_tab("Canvas")
    with c8:
        st.caption("ಕೋಡ್ ಮತ್ತು ನೋಟ್ಸ್ ಬರೆಯಿರಿ")

st.write("")

# Action Triggers
if st.session_state.active_tab == "Photos":
    st.subheader("🖼️ Photos & Image Studio")
    uploaded_file = st.file_uploader("ಫೋಟೋ ಅಪ್ಲೋಡ್ ಮಾಡಿ", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="ಮೂಲ ಫೋಟೋ", use_container_width=True)
        rot = st.slider("ತಿರುಗಿಸಿ", 0, 360, 0, 90)
        bright = st.slider("ಬೆಳಕು", 0.5, 2.0, 1.0, 0.1)
        bw = st.checkbox("Black & White")
        
        edited = img.rotate(rot)
        edited = ImageEnhance.Brightness(edited).enhance(bright)
        if bw:
            edited = edited.convert("L")
        st.image(edited, caption="ಎಡಿಟ್ ಆದ ಚಿತ್ರ", use_container_width=True)

elif st.session_state.active_tab == "Camera":
    st.subheader("📷 ಲೈವ್ ಕ್ಯಾಮೆರಾ")
    camera_photo = st.camera_input("ಸೆಲ್ಫಿ ಅಥವಾ ಫೋಟೋ ತೆಗೆದುಕೊಳ್ಳಿ")
    if camera_photo:
        st.image(camera_photo, caption="ಕ್ಯಾಪ್ಚರ್ ಮಾಡಿದ ಫೋಟೋ", use_container_width=True)

elif st.session_state.active_tab == "Videos":
    st.subheader("📹 Video Ideas")
    st.info("ಯಾವುದೇ ವೀಡಿಯೋ ಕಾನ್ಸೆಪ್ಟ್ ಬೇಕಿದ್ದರೆ ಕೆಳಗಿನ ಚಾಟ್‌ನಲ್ಲಿ ಕೇಳಿ!")

elif st.session_state.active_tab == "Music":
    st.subheader("🎵 Music Assistant")
    st.info("ಹಾಡಿನ ಸಾಹಿತ್ಯ ಅಥವಾ ಮ್ಯೂಸಿಕ್ ಐಡಿಯಾಗಳನ್ನು ಚಾಟ್‌ನಲ್ಲಿ ಕೇಳಿ!")

elif st.session_state.active_tab == "Canvas":
    st.subheader("📝 Nija Canvas")
    st.text_area("ನಿಮ್ಮ ನೋಟ್ಸ್ ಅಥವಾ ಕೋಡ್ ಅನ್ನು ಇಲ್ಲಿ ಬರೆಯಿರಿ:", height=200)

# Real AI Chat
user_query = st.chat_input("Ask NijaAI anything...")

if user_query:
    q_low = user_query.lower().strip()
    
    with st.chat_message("user"):
        st.write(user_query)
        
    with st.chat_message("assistant"):
        creator_words = ["creator", "founder", "owner", "developed", "who made", "ಯಾರು", "ಮಾಡಿದ್ದು", "ಹೆಸರು", "name"]
        if any(w in q_low for w in ["nija", "founder", "creator", "owner", "developed"]) and any(w in q_low for w in creator_words):
            st.markdown("🌟 **NijaAI** ಅನ್ನು ಅಭಿವೃದ್ಧಿಪಡಿಸಿದವರು ಮತ್ತು ಇದರ ಸಂಸ್ಥಾಪಕರು **Santhosh D (ಸಂತೋಷ್ ಡಿ)**.")
            
        elif any(op in user_query for op in ["+", "-", "*", "/", "%", "**"]) and any(c.isdigit() for c in user_query):
            try:
                ans = eval(user_query, {"__builtins__": None, "math": math})
                st.markdown(f"**ಉತ್ತರ:** `{ans}`")
            except Exception:
                pass
                
        else:
            with st.spinner("ಯೋಚಿಸುತ್ತಿದೆ..."):
                try:
                    system_prompt = (
                        "You are NijaAI, an authentic and smart AI built by Santhosh D. "
                        "Respond informatively, warmly, and intelligently in the same language as the user (Kannada or English). "
                        "Format responses cleanly with markdown."
                    )
                    full_prompt = f"{system_prompt}\n\nUser Question: {user_query}"
                    response = model.generate_content(full_prompt)
                    st.write(response.text)
                except Exception as e:
                    st.error(f"ದೋಷ: {e}")
