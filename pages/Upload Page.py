import streamlit as st
import base64
import sqlite3
import json
from datetime import datetime
import pandas as pd
import openai
import httpx
import pytz

st.set_page_config(page_title="🍱 Food Identifier & Calorie Tracker", layout="wide")
st.title("📸 Upload & Analyze Your Meal")

uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    col1, col2 = st.columns([1, 2])

    # Show uploaded image
    image_bytes = uploaded_file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    col1.image(image_bytes, caption="Uploaded Image")  # Removed use_container_width

    # Send to AI — updated OpenAI client with http_client
    client = openai.OpenAI(
        api_key="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",  # 🔐 Replace with your OpenRouter key
        http_client=httpx.Client(base_url="https://openrouter.ai/api/v1")
    )

    with col2:
        with st.spinner("Analyzing food image with AI..."):
            try:
                response = client.chat.completions.create(
                    model="meta-llama/llama-3.2-11b-vision-instruct:free",
                    messages=[
                        {"role": "system", "content": "Respond ONLY in valid JSON with food name and nutrition info."},
                        {"role": "user", "content": [
                            {"type": "text", "text": "Analyze this meal."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]}
                    ],
                    max_tokens=500
                )
                llm_text = response.choices[0].message.content.strip()
            except Exception as e:
                st.error(f"❌ API Error: {e}")
                st.stop()

        # Extract JSON safely
        first_brace = llm_text.find('{')
        last_brace = llm_text.rfind('}') + 1
        llm_text = llm_text[first_brace:last_brace]

        try:
            data = json.loads(llm_text)
        except json.JSONDecodeError:
            st.error("❌ JSON parse error")
            st.code(llm_text)
            st.stop()

        # Show Result
        st.success("✅ Nutritional Analysis")
        col2.markdown(f"**🍽️ Foods:** {', '.join(data.get('detected_foods', []))}")
        col2.markdown(f"**🔥 Calories:** {data.get('calories', 0)} kcal")
        col2.markdown(f"**💪 Protein:** {data.get('protein_g', 0)} g")
        col2.markdown(f"**🍞 Carbs:** {data.get('carbs_g', 0)} g")
        col2.markdown(f"**🧈 Fat:** {data.get('fat_g', 0)} g")
        col2.markdown(f"**🧪 Vitamins:** {', '.join(data.get('vitamins', []))}")

        # Save to SQLite
        ist = pytz.timezone('Asia/Kolkata')
        timestamp = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect("nutrition_log.db")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS food_nutrition (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                detected_foods TEXT,
                calories INTEGER,
                protein_g REAL,
                carbs_g REAL,
                fat_g REAL,
                vitamins TEXT,
                raw_llm_response TEXT,
                timestamp TEXT
            )
        """)
        conn.execute("""
            INSERT INTO food_nutrition (
                detected_foods, calories, protein_g, carbs_g, fat_g, vitamins, raw_llm_response, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ', '.join(data.get('detected_foods', [])),
            data.get('calories', 0),
            data.get('protein_g', 0.0),
            data.get('carbs_g', 0.0),
            data.get('fat_g', 0.0),
            ', '.join(data.get('vitamins', [])),
            llm_text,
            timestamp
        ))
        conn.commit()
        conn.close()

# Show history table
st.markdown("---")
st.subheader("📋 Last 5 Uploaded Meals")
conn = sqlite3.connect("nutrition_log.db")
df = pd.read_sql("SELECT * FROM food_nutrition ORDER BY id DESC LIMIT 5", conn)
st.dataframe(df.drop(columns=["raw_llm_response"]))
conn.close()
