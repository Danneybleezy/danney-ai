import streamlit as st
import requests
from PIL import Image
import base64
import io

# ------------------------
# CONFIG
# ------------------------
st.set_page_config(page_title="🤖 Danney AI", layout="centered")
st.title("🤖 Danney AI")
st.markdown("Your mobile AI powered by **Groq** + **Replicate** + **Voice** ✨")

# ------------------------
# SIDEBAR: Choose Mode
# ------------------------
mode = st.sidebar.radio("Choose Feature", ["🧠 Chat", "🖼️ Enhance Image", "🎤 Voice Assistant", "🎬 Video (Coming Soon)"])

# ------------------------
# KEYS
# ------------------------
GROQ_API_KEY = st.secrets["groq_api_key"]
REPLICATE_API_TOKEN = st.secrets["replicate_api_token"]

# ------------------------
# 🧠 Chat with Groq
# ------------------------
if mode == "🧠 Chat":
    st.subheader("💬 Ask Danney Anything")

    user_input = st.text_input("You:", placeholder="Type your question...")
    speak = st.checkbox("🔊 Read Danney's reply aloud")

    if user_input:
        with st.spinner("Danney is thinking..."):
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            body = {
                "model": "llama3-70b-8192",
                "messages": [
                    {"role": "system", "content": "You are Danney, a helpful assistant."},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.7,
                "max_tokens": 1024,
                "stream": False
            }
            res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body)
            result = res.json()

            if "choices" in result:
                reply = result["choices"][0]["message"]["content"]
                st.markdown(f"**Danney:** {reply}")
                if speak:
                    st.markdown(f'<audio autoplay src="https://api.streamelements.com/kappa/v2/speech?voice=Brian&text={requests.utils.quote(reply)}"></audio>', unsafe_allow_html=True)
            else:
                st.error("❌ Chat failed: " + str(result.get("error", "Unknown error")))

# ------------------------
# 🖼️ Image Enhancer
# ------------------------
elif mode == "🖼️ Enhance Image":
    st.subheader("🖼️ Upload a photo to enhance (face restoration)")

    uploaded_file = st.file_uploader("Choose image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Original", use_column_width=True)

        if st.button("✨ Enhance"):
            with st.spinner("Enhancing image..."):
                try:
                    output_url = requests.post(
                        "https://api.replicate.com/v1/predictions",
                        headers={
                            "Authorization": f"Token {REPLICATE_API_TOKEN}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "version": "92843753e1e52cdb6c7c3f3e1e41dbd2dfb0b37b13b017db61e028e2f9d8cb0b",
                            "input": {"img": uploaded_file.getvalue()}
                        }
                    ).json()

                    image_url = output_url.get("output", [None])[0]
                    if image_url:
                        enhanced = Image.open(requests.get(image_url, stream=True).raw)
                        st.image(enhanced, caption="Enhanced Image", use_column_width=True)
                    else:
                        st.error("Enhancement failed.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ------------------------
# 🎤 Voice Assistant (Input via Mic + Chat)
# ------------------------
elif mode == "🎤 Voice Assistant":
    st.subheader("🎤 Speak to Danney (via mic)")

    st.markdown("""
    > 📌 Voice input works best in a **desktop browser** or **mobile browser with mic support**.
    """)

    st.markdown("Try using [https://speech-to-text-demo.vercel.app](https://speech-to-text-demo.vercel.app) to get your voice transcribed.")

    text_input = st.text_area("Paste your speech-to-text result here:")

    if st.button("🧠 Ask Danney"):
        if not text_input.strip():
            st.warning("Please paste your voice text.")
        else:
            with st.spinner("Danney is replying..."):
                headers = {
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                }
                body = {
                    "model": "llama3-70b-8192",
                    "messages": [
                        {"role": "system", "content": "You are Danney, a helpful assistant."},
                        {"role": "user", "content": text_input}
                    ]
                }
                res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body)
                reply = res.json()["choices"][0]["message"]["content"]
                st.markdown(f"**Danney:** {reply}")
                st.markdown(f'<audio autoplay src="https://api.streamelements.com/kappa/v2/speech?voice=Brian&text={requests.utils.quote(reply)}"></audio>', unsafe_allow_html=True)

# ------------------------
# 🎬 Video Generation Placeholder
# ------------------------
elif mode == "🎬 Video (Coming Soon)":
    st.subheader("🎬 AI Video Generation (Coming Soon!)")
    st.info("This feature will let Danney turn images + text into cinematic videos using tools like Runway or Pika Labs.")
