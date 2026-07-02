import streamlit as st
import google.generativeai as genai

st.title("🎬 កម្មវិធីបកប្រែរឿងចិន")

# ដាក់ប្រអប់សម្រាប់ API Key
api_key = st.text_input("បញ្ចូល Gemini API Key:", type="password")
text = st.text_area("វាយអត្ថបទរឿងចិន៖")

if st.button("បកប្រែជាភាសាខ្មែរ"):
    if api_key and text:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"បកប្រែអត្ថបទនេះទៅខ្មែរ: {text}")
        st.success(res.text)
    else:
        st.error("សូមបញ្ចូល API Key និងអត្ថបទ")

