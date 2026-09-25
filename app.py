import streamlit as st
import math
from PIL import Image, ImageEnhance, ImageFilter
from duckduckgo_search import DDGS

st.set_page_config(page_title="NijaAI - Smart City & Studio", page_icon="⚡", layout="wide")
st.title("⚡ NijaAI (ನಿಜ AI)")
st.caption("Developed by Santhosh D | ಸ್ಮಾರ್ಟ್ ಲೈವ್ ಸರ್ಚ್ • ಎ ಟು ಝಡ್ ಗೈಡ್ • ನಿಖರ ಲೆಕ್ಕಾಚಾರ • ಫೋಟೋ ಸ್ಟುಡಿಯೋ")

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

# Main Search & Logic
query = st.text_input("ಸರ್ಚ್ ಮಾಡಿ ಅಥವಾ ಲೆಕ್ಕ ನಮೂದಿಸಿ:")

if st.button("Search / Run") and query:
    q_lower = query.lower().strip()
    
    # 1. Creator / Founder Check
    creator_keywords = ["creat", "founder", "owner", "developed", "ಯಾರು", "ಮಾಡಿದ್ದು", "ಯಾರ", "ಹೆಸರು", "name"]
    if any(k in q_lower for k in ["creat", "founder", "owner", "nija ai", "nijaai"]) and any(k in q_lower for k in creator_keywords):
        st.subheader("👑 NijaAI ಪರಿಚಯ")
        st.success("🌟 **NijaAI (ನಿಜ AI)** ಅನ್ನು ಅಭಿವೃದ್ಧಿಪಡಿಸಿದವರು ಮತ್ತು ಇದರ ಸಂಸ್ಥಾಪಕರು **Santhosh D (ಸಂತೋಷ್ ಡಿ)**.")
        st.info("NijaAI ಎಂಬುದು ಸ್ಮಾರ್ಟ್ ಲೈವ್ ವೆಬ್ ಸರ್ಚ್, ನಿಖರ ಲೆಕ್ಕಾಚಾರ ಮತ್ತು ಇಮೇಜ್ ಸ್ಟುಡಿಯೋ ಒದಗಿಸುವ ವೇಗದ ಎಐ ಪ್ಲಾಟ್‌ಫಾರ್ಮ್ ಆಗಿದೆ.")
        
    # 2. Math Calculation
    elif any(op in query for op in ["+", "-", "*", "/", "%", "**"]) and any(char.isdigit() for char in query):
        st.subheader("🔢 ನಿಖರ ಲೆಕ್ಕಾಚಾರದ ಫಲಿತಾಂಶ")
        try:
            result = eval(query, {"__builtins__": None, "math": math})
            st.success(f"**ಲೆಕ್ಕ:** `{query}`  \n**ಉತ್ತರ:** `{result}`")
        except Exception as e:
            st.error(f"ಲೆಕ್ಕಾಚಾರದಲ್ಲಿ ದೋಷ: {e}")
            
    # 3. Live Web Search
    else:
        st.subheader("🌐 AI ಸಮಗ್ರ ವಿವರ (A to Z Guide)")
        with st.spinner("ಮಾಹಿತಿ ಸಂಗ್ರಹಿಸಲಾಗುತ್ತಿದೆ..."):
            try:
                results = []
                with DDGS() as ddgs:
                    for r in ddgs.text(query, max_results=5):
                        results.append(r)
                
                if results:
                    for item in results:
                        st.markdown(f"### [{item.get('title')}]({item.get('href')})")
                        st.write(item.get("body"))
                        st.divider()
                else:
                    st.warning("ಯಾವುದೇ ಫಲಿತಾಂಶಗಳು ಕಂಡುಬಂದಿಲ್ಲ.")
            except Exception as e:
                st.error(f"ದೋಷ: {e}")
