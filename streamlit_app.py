import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Page config
st.set_page_config(page_title="🎬 បកប្រែរឿង", layout="wide")

st.title("🎬 កម្មវិធីបកប្រែរឿង")
st.markdown("បកប្រែរឿងចិន និងខ្មែរ ដោយប្រើ Gemini AI")

# Sidebar for API Key
with st.sidebar:
    st.header("⚙️ ការកំណត់")
    api_key = st.text_input("បញ្ចូល Gemini API Key:", type="password", key="api_key")
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.success("✅ API Key ត្រឹមត្រូវ")
        except:
            st.error("❌ API Key មិនត្រឹមត្រូវ")
    
    st.markdown("---")
    st.info("💡 ទទួលបាន API Key នៅ: https://makersuite.google.com/app/apikey")

# Main content - Two columns
col1, col2 = st.columns(2)

with col1:
    st.header("📝 ប្រភព")
    
    # Language selection
    source_lang = st.selectbox(
        "ភាសាប្រភព:",
        ["ចិន (Chinese)", "ខ្មែរ (Khmer)", "ឧទ្ធម្ភាគ (English)"]
    )
    
    source_text = st.text_area(
        "វាយ ឬ ដាក់ពេលបិទ អត្ថបទ:",
        height=250,
        placeholder="ឧ. ឧទាហរណ៍អត្ថបទនឹងលេចឡើងនៅទីនេះ..."
    )

with col2:
    st.header("🎯 គោលដៅ")
    
    # Target language selection
    target_lang = st.selectbox(
        "ភាសាគោលដៅ:",
        ["ខ្មែរ (Khmer)", "ចិន (Chinese)", "ឧទ្ធម្ភាគ (English)"],
        index=0
    )
    
    # Output area
    translated_text = st.text_area(
        "ផលលទ្ធិបកប្រែ:",
        height=250,
        disabled=True,
        value=st.session_state.get("translated_result", ""),
        key="output"
    )

# Validation warning
if source_lang == target_lang:
    st.warning("⚠️ សូមជ្រើសរើសភាសាខុសគ្នា")

# Translation button
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    if st.button("🚀 បកប្រែឥឡូវនេះ", use_container_width=True):
        if not api_key:
            st.error("❌ សូមបញ្ចូល API Key ដំបូង")
        elif not source_text:
            st.error("❌ សូមបញ្ចូលអត្ថបទដែលត្រូវបកប្រែ")
        elif source_lang == target_lang:
            st.error("❌ ភាសាប្រភព និងគោលដៅត្រូវតែខុសគ្នា")
        else:
            with st.spinner("⏳ កំពុងបកប្រែ..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Create translation prompt with proper language mapping
                    lang_map = {
                        "ចិន (Chinese)": "Chinese",
                        "ខ្មែរ (Khmer)": "Khmer",
                        "ឧទ្ធម្ភាគ (English)": "English"
                    }
                    
                    source = lang_map.get(source_lang, source_lang)
                    target = lang_map.get(target_lang, target_lang)
                    
                    prompt = f"Translate the following text from {source} to {target} while preserving the original meaning, tone, and style. Do not add any additional commentary or explanations.\n\nText to translate:\n{source_text}"
                    
                    response = model.generate_content(prompt)
                    translation = response.text
                    
                    # Save to session state for display
                    st.session_state.translated_result = translation
                    
                    # Save to history
                    if 'history' not in st.session_state:
                        st.session_state.history = []
                    
                    st.session_state.history.append({
                        'timestamp': datetime.now(),
                        'source': source_lang,
                        'target': target_lang,
                        'original': source_text,
                        'translated': translation
                    })
                    
                    # Display result
                    st.success("✅ បកប្រែបានដោះស្រាយ!")
                    st.rerun()
                    
                except genai.types.APIError as e:
                    st.error(f"❌ កំហុស API: {str(e)}")
                except Exception as e:
                    st.error(f"❌ កំហុស: {str(e)}")

# Translation history
st.markdown("---")
st.header("📚 ប្រវត្តិការបកប្រែ")

if 'history' in st.session_state and st.session_state.history:
    for i, item in enumerate(reversed(st.session_state.history[-5:]), 1):  # Show last 5
        with st.expander(f"📖 ការបកប្រែលេខ {i} - {item['timestamp'].strftime('%H:%M:%S')}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**ភាសាប្រភព:** {item['source']}")
                st.text(item['original'][:100] + "..." if len(item['original']) > 100 else item['original'])
            with col2:
                st.write(f"**ភាសាគោលដៅ:** {item['target']}")
                st.text(item['translated'][:100] + "..." if len(item['translated']) > 100 else item['translated'])
else:
    st.info("💭 មិនមានប្រវត្តិការបកប្រែឡើយ")
