import streamlit as st
import openai

# Page setup
st.set_page_config(page_title="🤖 Nutrition Chatbot", layout="wide")
st.title("🥦 AI Nutrition Chat Assistant")

# OpenRouter API setup
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"  # 🔁 Replace with your actual OpenRouter API key
)

# Session state to hold messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful nutrition assistant. Answer only questions related to food, "
                "macronutrients (calories, protein, carbs, fat), vitamins, or health nutrition. "
                "If a user asks something unrelated (e.g., weather, sports), say: "
                "'❌ I'm a nutrition assistant. I can only help with food and nutrition topics.'"
            )
        },
        {
            "role": "assistant",
            "content": (
                "👋 Hello! I'm your personal AI Nutrition Assistant. Ask me anything about food, calories, protein, fat, carbs, or vitamins!"
            )
        }
    ]

# Show conversation
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])

# Chat input box
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
                        "HTTP-Referer": "https://your-app.com",
                        "X-Title": "NutriBot"
                    }
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"❌ API Error: {e}"

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
