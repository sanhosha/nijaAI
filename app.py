import streamlit as st
import math
from PIL import Image, ImageEnhance, ImageFilter
from duckduckgo_search import DDGS
from groq import Groq

# Groq API Key (ನಿಮ್ಮ API ಕೀಯನ್ನು ಇಲ್ಲಿ ಪೇಸ್ಟ್ ಮಾಡಿ)
GROQ_API_KEY = "ಇಲ್ಲಿ_ನಿಮ್ಮ_GROQ_API_KEY_ಹಾಕಿ"

st.set_page_config(page_title="NijaAI - Smart AI & Studio", page_icon="⚡", layout="wide")
st.title("⚡ NijaAI (ನಿಜ AI)")
st.caption("Developed by Santhosh D | AI ಉತ್ತರ • ಲೈವ್ ವೆಬ್ ಸರ್ಚ್ • ಲೆಕ್ಕಾಚಾರ • ಫೋಟೋ ಸ್ಟುಡಿಯೋ")

# Sidebar - Image Studio
st.sidebar.header("🎨 ಫೋಟೋ ಸ್ಟುಡಿಯೋ (Image Studio)")
uploaded_file = st.sidebar.file_uploader("ಫೋಟೋ ಅಪ್ಲೋಡ್ ಮಾಡಿ", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.sidebar.image(image, caption="ಮೂಲ ಫೋಟೋ", use_container_width=True)
    
    st.sidebar.subheader("ಎಡಿಟಿಂಗ್")
    rotation = st.sidebar.slider("ತಿರುಗಿಸಿ", 0, 360, 0, 90)
    brightness = st.sidebar.slider("ಬೆಳಕು", 0.5, 2.0, 1.0, 0.1)
    contrast = st.sidebar.slider("ಕಾಂಟ್ರಾಸ್ಟ್", 0.5, 2.0, 1.0, 0.1)
    apply_blur = st.sidebar.checkbox("Blur Filter")
    apply_grayscale = st.sidebar.checkbox("Black & White")
    
    edited_image = image.rotate(rotation)
    enhancer_b = ImageEnhance.Brightness(edited_image)
    edited_image = enhancer_b.enhance(brightness)
    enhancer_c = ImageEnhance.Contrast(edited_image)
    edited_image = enhancer_c.enhance(contrast)
    
    if apply_blur:
        edited_image = edited_image.filter(ImageFilter.BLUR)
    if apply_grayscale:
        edited_image = edited_image.convert("L")
        
    st.sidebar.image(edited_image, caption="ಎಡಿಟ್ ಆದ ಫೋಟೋ", use_container_width=True)

# Main Interaction
query = st.text_input("ನಿಮ್ಮ ಪ್ರಶ್ನೆ ಕೇಳಿ ಅಥವಾ ಲೆಕ್ಕ ನಮೂದಿಸಿ:")

if st.button("Search / Ask") and query:
    q_lower = query.lower().strip()
    
    # 1. Creator / Founder Rule
    creator_keywords = ["creat", "founder", "owner", "developed", "ಯಾರು", "ಮಾಡಿದ್ದು", "ಯಾರ", "ಹೆಸರು", "name"]
    if any(k in q_lower for k in ["creat", "founder", "owner", "nija ai", "nijaai"]) and any(k in q_lower for k in creator_keywords):
        st.subheader("👑 NijaAI ಪರಿಚಯ")
        st.success("🌟 **NijaAI (ನಿಜ AI)** ಅನ್ನು ಅಭಿವೃದ್ಧಿಪಡಿಸಿದವರು ಮತ್ತು ಇದರ ಸಂಸ್ಥಾಪಕರು **Santhosh D (ಸಂತೋಷ್ ಡಿ)**.")
        st.info("NijaAI ಅತ್ಯಾಧುನಿಕ AI ಚಾಟ್, ವೆಬ್ ಮಾಹಿತಿ ಮತ್ತು ಫೋಟೋ ಎಡಿಟಿಂಗ್ ಒದಗಿಸುವ ವೇಗದ ಎಐ ಪ್ಲಾಟ್‌ಫಾರ್ಮ್ ಆಗಿದೆ.")
        
    # 2. Math Calculation
    elif any(op in query for op in ["+", "-", "*", "/", "%", "**"]) and any(char.isdigit() for char in query):
        st.subheader("🔢 ನಿಖರ ಲೆಕ್ಕಾಚಾರದ ಫಲಿತಾಂಶ")
        try:
            result = eval(query, {"__builtins__": None, "math": math})
            st.success(f"**ಲೆಕ್ಕ:** `{query}`  \n**ಉತ್ತರ:** `{result}`")
        except Exception as e:
            st.error(f"ಲೆಕ್ಕಾಚಾರದಲ್ಲಿ ದೋಷ: {e}")
            
    # 3. Direct AI Answer for everything else
    else:
        st.subheader("🤖 NijaAI ಉತ್ತರ")
        with st.spinner("ಯೋಚಿಸುತ್ತಿದೆ..."):
            try:
                # ಲೈವ್ ಸರ್ಚ್ ಮಾಹಿತಿ ಸಂಗ್ರಹ
                web_context = ""
                with DDGS() as ddgs:
                    for r in ddgs.text(query, max_results=3):
                        web_context += f"- {r.get('title')}: {r.get('body')}\n"
                
                # Groq AI ಮೂಲಕ ಉತ್ತರ ರಚನೆ
                client = Groq(api_key=GROQ_API_KEY)
                system_prompt = (
                    "You are NijaAI, an intelligent assistant built by Santhosh D. "
                    "Answer clearly, informatively, and accurately in the requested language (Kannada or English). "
                    "Use the provided web context if relevant."
                )
                user_msg = f"Question: {query}\n\nWeb context (if needed):\n{web_context}"
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_msg}
                    ]
                )
                
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"ಉತ್ತರ ಪಡೆಯುವಲ್ಲಿ ದೋಷ: {e}")
