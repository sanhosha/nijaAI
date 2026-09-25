import streamlit as st
import math
from PIL import Image, ImageEnhance, ImageFilter
from langchain_community.llms import Ollama
from duckduckgo_search import DDGS

st.set_page_config(page_title="NijaAI - Smart City & Studio", page_icon="⚡", layout="wide")
st.title("⚡ NijaAI (ನಿಜ AI)")
st.caption("ಸ್ಮಾರ್ಟ್ ಲೈವ್ ಸರ್ಚ್ • ಎ ಟು ಝಡ್ ಗೈಡ್ • ನಿಖರ ಲೆಕ್ಕಾಚಾರ • ಫೋಟೋ ಸ್ಟುಡಿಯೋ")

# Sidebar - Image Studio
st.sidebar.header("🖼️ ಫೋಟೋ ಎಡಿಟಿಂಗ್ (Image Studio)")
uploaded_file = st.sidebar.file_uploader("ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.sidebar.image(image, caption="ಮೂಲ ಫೋಟೋ", use_column_width=True)
    
    st.sidebar.subheader("ಟೂಲ್ಸ್")
    rotation = st.sidebar.slider("ತಿರುಗಿಸಿ", 0, 360, 0, 90)
    brightness = st.sidebar.slider("ಬೆಳಕು", 0.5, 2.0, 1.0, 0.1)
    contrast = st.sidebar.slider("ಕಾಂಟ್ರಾಸ್ಟ್", 0.5, 2.0, 1.0, 0.1)
    apply_blur = st.sidebar.checkbox("Blur Filter")
    apply_grayscale = st.sidebar.checkbox("Black & White")

    edited_img = image.rotate(rotation, expand=True)
    edited_img = ImageEnhance.Brightness(edited_img).enhance(brightness)
    edited_img = ImageEnhance.Contrast(edited_img).enhance(contrast)
    
    if apply_blur:
        edited_img = edited_img.filter(ImageFilter.BLUR)
    if apply_grayscale:
        edited_img = edited_img.convert("L")

    st.subheader("ಎಡಿಟ್ ಮಾಡಿದ ಫೋಟೋ:")
    st.image(edited_img, use_column_width=True)

st.markdown("---")

@st.cache_resource
def get_llm():
    return Ollama(model="llama3.2", temperature=0.1)

def safe_calc(expr):
    try:
        allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        return str(eval(expr, {"__builtins__": {}}, allowed))
    except Exception as e:
        return f"Error: {e}"

# Search Box
query = st.text_input("ಸರ್ಚ್ ಮಾಡಿ ಅಥವಾ ಲೆಕ್ಕ ನಮೂದಿಸಿ:", placeholder="ಉದಾ: bengaluru, chatgpt, 5420 * 18")

if st.button("Search / Run") and query:
    if any(char in query for char in "+-*/") and any(char.isdigit() for char in query):
        res = safe_calc(query)
        st.success(f"🔢 ನಿಖರ ಲೆಕ್ಕಾಚಾರ: {query} = {res}")
    else:
        with st.spinner("ಮಾಹಿತಿ ಸಂಗ್ರಹಿಸಿ ಸಿದ್ಧಪಡಿಸಲಾಗುತ್ತಿದೆ..."):
            try:
                results = []
                with DDGS() as ddgs:
                    search_term = f"{query} hotels cafes events news" if len(query.split()) == 1 else query
                    for r in ddgs.text(search_term, max_results=5):
                        results.append(r)

                if results:
                    st.subheader("🤖 AI ಸಮಗ್ರ ವಿವರ (A to Z Guide)")
                    context_text = "\n".join([f"- {item['title']}: {item['body']}" for item in results])
                    
                    llm = get_llm()
                    prompt = f"""
                    User searched for: {query}
                    Search Context:
                    {context_text}

                    Instructions:
                    - If the query is a city/place (e.g. bengaluru), provide a structured breakdown:
                      1. Overview of the place
                      2. Top Iconic Hotels & Traditional Tiffin spots
                      3. Trending & Best Cafes
                      4. Present updates (current events, metro, weather)
                      5. Upcoming events & future developments
                    - If it's a topic/tool (e.g. chatgpt), provide a direct, clear factual explanation.
                    Provide clear response in conversational Kannada or simple English.
                    """
                    summary = llm.invoke(prompt)
                    st.info(summary)

                    st.subheader("🌐 ಗೂಗಲ್ ಮಾದರಿಯ ವೆಬ್ ಲಿಂಕ್‌ಗಳು (Web Results)")
                    for item in results:
                        st.markdown(f"### [{item['title']}]({item['href']})")
                        st.caption(item['href'])
                        st.write(item['body'])
                        st.divider()
                else:
                    st.warning("ಯಾವುದೇ ಫಲಿತಾಂಶ ದೊರೆತಿಲ್ಲ.")

            except Exception as e:
                st.error(f"ದೋಷ: {e}")