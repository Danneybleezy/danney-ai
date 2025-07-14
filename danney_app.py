import streamlit as st
import requests
import os

# UI setup
st.set_page_config(page_title="🤖 Danney AI", layout="centered")
st.title("🤖 Danney AI")
st.markdown("Your lightning-fast mobile assistant powered by Groq 🚀")

# Input
user_input = st.text_input("You:", placeholder="Ask me anything...")

# On input
if user_input:
    with st.spinner("Danney is thinking..."):
        try:
            headers = {
                "Authorization": f"Bearer {st.secrets['groq_api_key']}",
                "Content-Type": "application/json"
            }
            body = {
                "model": "mixtral-8x7b-32768",  # You can also try llama3-70b-8192
                "messages": [
                    {"role": "system", "content": "You are Danney, a helpful mobile assistant."},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.7,
                "max_tokens": 1024,
                "stream": False
            }

            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body)
            result = response.json()

            if "choices" in result:
                answer = result["choices"][0]["message"]["content"]
                st.markdown(f"**Danney:** {answer}")
            else:
                st.error(f"Failed to get response: {result}")

        except Exception as e:
            st.error(f"Error: {str(e)}")
