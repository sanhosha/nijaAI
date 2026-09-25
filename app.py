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

# Dark Minimal Styling
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
        margin: 15px 0 25px 0;
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

# Gemini Drawer Menu (Clean Native Streamlit Components)
with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("🖼️ Photos", use_container_width=True)
    with col2:
        st.button("📷 Camera", use_container_width=True)
    with col3:
        st.button("✨ Avatar", use_container_width=True)

    st.divider()

    st.markdown("🎨 **Images**  \n:grey[Create and edit]")
    st.markdown("📹 **Videos**  \n:grey[Bring ideas to life]")
    st.markdown("🎵 **Music**  \n:grey[Make audio tracks]")
    st.markdown("📝 **Canvas**  \n:grey[Code, write or make slides]")

# Photo Editing Section
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

# Chat Input & Responses
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
