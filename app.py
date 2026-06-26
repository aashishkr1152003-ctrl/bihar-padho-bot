import streamlit as st
from openai import OpenAI

# ===== तेरा कंट्रोल पैनल - यहाँ अपना नंबर/UPI बदल =====
BOT_NAME = "Bihar Padho Bot"
PRICE = "₹99/महीना" 
UPI_ID = "aashish@paytm" # यहाँ अपना UPI डाल दे
WHATSAPP_NUMBER = "919876543210" # यहाँ अपना 10-digit नंबर डाल दे

SYSTEM_PROMPT = """
तुम Bihar Board 10th और 12th के स्टूडेंट्स के लिए AI टीचर हो।
नाम: Bihar Padho Bot
स्टाइल: दोस्त की तरह, आसान हिंदी में, बिहारी टच के साथ
रूल:
1. सिर्फ Bihar Board SCERT syllabus से जवाब दो
2. अगर सवाल सिलेबस से बाहर है तो बोलो "भाई ये 10th-12th में नहीं है"
3. हर जवाब के बाद एक MCQ पूछो प्रैक्टिस के लिए
"""

client = OpenAI(
    api_key = st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)
# ================================================

st.set_page_config(page_title=BOT_NAME, page_icon="📚")
st.title(f"📚 {BOT_NAME}")
st.markdown(f"**{PRICE} में अनलिमिटेड डाउट पूछो**")

with st.sidebar:
    st.header("🔓 Full Access लो")
    st.write("फ्री में 3 सवाल रोज। अनलिमिटेड के लिए:")
    st.code(f"UPI: {UPI_ID}")
    st.write(f"पे करके स्क्रीनशॉट भेजो: {WHATSAPP_NUMBER}")
    st.link_button("WhatsApp पे भेजो", f"https://wa.me/{WHATSAPP_NUMBER}")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.count = 0

for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("10th/12th का कोई भी डाउट पूछो..."):
    if st.session_state.count >= 3:
        st.error("फ्री लिमिट खत्म! अनलिमिटेड के लिए पेमेंट करो ⬅️")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    st.session_state.count += 1

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.messages
    )
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
