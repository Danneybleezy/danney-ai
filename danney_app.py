import streamlit as st
import requests

# ---- Page Config ----
st.set_page_config(page_title="🤖 Danney AI", layout="centered")
st.title("🤖 Danney AI")
st.markdown("Your lightning-fast mobile assistant powered by **Groq (LLaMA 3)** 🚀")

# ---- User Input ----
user_input = st.text_input("You:", placeholder="Ask me anything...")

# ---- On Input ----
if user_input:
    with st.spinner("Danney is thinking..."):
        try:
            headers = {
                "Authorization": f"Bearer {st.secrets['groq_api_key']}",
                "Content-Type": "application/json"
            }

            body = {
                "model": "llama3-70b-8192",  # ✅ Current active Groq model
                "messages": [
                    {"role": "system", "content": "You are Danney, a helpful and friendly mobile assistant."},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.7,
                "max_tokens": 1024,
                "stream": False
            }

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=body
            )

            result = response.json()

            if "choices" in result:
                reply = result["choices"][0]["message"]["content"]
                st.markdown(f"**Danney:** {reply}")
            else:
                st.error(f"❌ Failed to get response: {result.get('error', 'Unknown error')}")
        
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
