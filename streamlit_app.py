import streamlit as st
import google.generativeai as genai

st.title("🎬 កម្មវិធីបកប្រែរឿងចិន")

# ដាក់ប្រអប់សម្រាប់ API Key
api_key = st.text_input("បញ្ចូល Gemini API Key:", type="password")
text = st.text_area("វាយអត្ថបទរឿងចិន៖")

# Language selection
source_lang = st.selectbox("ភាសាប្រភព:", ["ចិន", "ខ្មែរ"])
target_lang = st.selectbox("ភាសាគោលដៅ:", ["ខ្មែរ", "ចិន"])

if st.button("បកប្រែ"):
    if api_key and text:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content(f"បកប្រែអត្ថបទនេះពី{source_lang}ទៅ{target_lang}: {text}")
            st.success(res.text)
        except Exception as e:
            st.error(f"កំហុស: {str(e)}")
    else:
        st.error("សូមបញ្ចូល API Key និងអត្ថបទ")
