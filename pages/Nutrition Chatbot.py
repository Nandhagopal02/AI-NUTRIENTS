import streamlit as st
import openai
import httpx
import os

# Page setup
st.set_page_config(page_title="🤖 Nutrition Chatbot", layout="wide")
st.title("🥦 AI Nutrition Chat Assistant")

# Secure OpenRouter API setup
client = openai.OpenAI(
    api_key=os.getenv("OPENROUTER_KEY"),  # 🔐 Set this in Render → Environment Variables
    http_client=httpx.Client(base_url="https://openrouter.ai/api/v1")
)

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful nutrition assistant. Respond only to questions about food, "
                "calories, macronutrients, vitamins, or nutrition. If asked something unrelated, reply: "
                "'❌ I'm a nutrition assistant. I only help with food and nutrition topics.'"
            )
        },
        {
            "role": "assistant",
            "content": (
                "👋 Hello! I'm your AI Nutrition Assistant. Ask me about calories, protein, fat, carbs, or vitamins!"
            )
        }
    ]

# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Input box
user_input = st.chat_input("Ask a nutrition question...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="meta-llama/llama-3.2-11b-vision-instruct:free",
                    messages=st.session_state.messages,
                    max_tokens=500,
                    extra_headers={
                        "HTTP-Referer": "https://your-app.com",  # optional
                        "X-Title": "NutriBot"
                    }
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"❌ API Error: {e}"

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
