import streamlit as st
import math
from PIL import Image, ImageEnhance
from duckduckgo_search import DDGS

st.set_page_config(
    page_title="NijaAI - Gemini Edition", 
    page_icon="✦", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Styling & UI Layout
html_layout = """
<style>
    .stApp {
        background-color: #0e0e10;
        color: #f0f0f0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 20px;
    }
    .brand {
        font-size: 1.15rem;
        font-weight: 500;
        color: #d1d5db;
    }
    .profile-pill {
        background-color: #d9532f;
        color: white;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }
    .hero {
        text-align: center;
        margin: 10px 0 20px 0;
    }
    .sparkle {
        font-size: 2.4rem;
        background: linear-gradient(45deg, #4285F4, #9B72CB, #D96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    .jump-in {
        font-size: 1.85rem;
        font-weight: 500;
        color: #e5e7eb;
        margin-top: 4px;
    }
    .credit {
        color: #9ca3af;
        font-size: 0.82rem;
        margin-top: 3px;
    }
    .drawer-card {
        background-color: #1a1a1c;
        border-radius: 28px;
        padding: 20px 18px;
        margin-top: 15px;
        border: 1px solid #28282b;
    }
    .drawer-handle {
        width: 36px;
        height: 4px;
        background-color: #4b5563;
        border-radius: 4px;
        margin: 0 auto 18px auto;
    }
    .actions-grid {
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
    }
    .action-item {
        background-color: #242427;
        border-radius: 20px;
        width: 76px;
        height: 76px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 5px;
        font-size: 0.78rem;
        color: #d1d5db;
        border: 1px solid #323236;
    }
    .feature-row {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 10px 6px;
    }
    .feature-icon {
        font-size: 1.4rem;
        width: 30px;
        text-align: center;
    }
    .feature-title {
        font-size: 0.98rem;
        font-weight: 500;
        color: #f3f4f6;
    }
    .feature-desc {
        font-size: 0.78rem;
        color: #9ca3af;
    }
</style>

<div class="top-nav">
    <div class="brand">Gemini Flash <span style="font-size: 0.7rem; color: #60a5fa;">●</span></div>
    <div class="profile-pill">S</div>
</div>

<div class="hero">
    <div class="sparkle">✦</div>
    <div class="jump-in">Let’s jump in, Santhu</div>
    <div class="credit">Developed by Santhosh D</div>
</div>

<div class="drawer-card">
    <div class="drawer-handle"></div>
    <div class="actions-grid">
        <div class="action-item"><span style="font-size: 1.3rem;">🖼️</span>Photos</div>
        <div class="action-item"><span style="font-size: 1.3rem;">📷</span>Camera</div>
        <div class="action-item"><span style="font-size: 1.3rem;">✨</span>Avatar</div>
    </div>
    
    <div class="feature-row">
        <div class="feature-icon">🎨</div>
        <div>
            <div class="feature-title">Images</div>
            <div class="feature-desc">Create and edit</div>
        </div>
    </div>
    <div class="feature-row">
        <div class="feature-icon">📹</div>
        <div>
            <div class="feature-title">Videos</div>
            <div class="feature-desc">Bring ideas to life</div>
        </div>
    </div>
    <div class="feature-row">
        <div class="feature-icon">🎵</div>
        <div>
            <div class="feature-title">Music</div>
            <div class="feature-desc">Make audio tracks</div>
        </div>
    </div>
    <div class="feature-row">
        <div class="feature-icon">📝</div>
        <div>
            <div class="feature-title">Canvas</div>
            <div class="feature-desc">Code, write or make slides</div>
        </div>
    </div>
</div>
<br>
"""

st.markdown(html_layout, unsafe_allow_html=True)

# Image Studio in expander
with st.expander("📸 ಫೋಟೋ ಎಡಿಟಿಂಗ್ ತೆರೆಯಿರಿ (Image Studio)"):
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

# Bottom Interactive Chat Input
user_query = st.chat_input("Ask NijaAI anything...")

if user_query:
    q_low = user_query.lower().strip()
    
    with st.chat_message("user"):
        st.write(user_query)
        
    with st.chat_message("assistant"):
        creator_words = ["creator", "founder", "owner", "developed", "who made", "ಯಾರು", "ಮಾಡಿದ್ದು", "ಹೆಸರು"]
        if any(w in q_low for w in ["nija", "founder", "creator", "owner", "developed"]) and any(w in q_low for w in creator_words):
            st.markdown("🌟 **NijaAI** ಅನ್ನು ಅಭಿವೃದ್ಧಿಪಡಿಸಿದವರು ಮತ್ತು ಇದರ ಸಂಸ್ಥಾಪಕರು **Santhosh D (ಸಂತೋಷ್ ಡಿ)**.")
            
        elif any(op in user_query for op in ["+", "-", "*", "/", "%", "**"]) and any(c.isdigit() for c in user_query):
            try:
                ans = eval(user_query, {"__builtins__": None, "math": math})
                st.markdown(f"**ಉತ್ತರ:** `{ans}`")
            except Exception as e:
                st.error(f"ಲೆಕ್ಕಾಚಾರ ದೋಷ: {e}")
                
        else:
            with st.spinner("ಹುಡುಕಲಾಗುತ್ತಿದೆ..."):
                try:
                    res_texts = []
                    with DDGS() as ddgs:
                        for item in ddgs.text(user_query, max_results=3):
                            if item.get("body"):
                                res_texts.append(item.get("body"))
                    if res_texts:
                        st.write(" ".join(res_texts))
                    else:
                        st.info("ಕ್ಷಮಿಸಿ, ಈ ಬಗ್ಗೆ ಯಾವುದೇ ಮಾಹಿತಿ ಸಿಗಲಿಲ್ಲ.")
                except Exception as e:
                    st.error(f"ದೋಷ: {e}")
