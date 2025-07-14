import streamlit as st
import base64
import sqlite3
import json
from datetime import datetime
import pandas as pd
import openai
import pytz

st.set_page_config(page_title="🍱 Food Identifier & Calorie Tracker", layout="centered")
st.title("🥗 Upload Food Image to Analyze")

uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image_bytes = uploaded_file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    st.image(image_bytes, caption="Uploaded Image", use_container_width=True)

    client = openai.OpenAI(
        api_key="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",
        base_url="https://openrouter.ai/api/v1"
    )

    with st.spinner("Analyzing food image..."):
        try:
            response = client.chat.completions.create(
                model="meta-llama/llama-3.2-11b-vision-instruct:free",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a food and nutrition assistant. Respond ONLY in this exact JSON format:\n\n"
                            "{\n"
                            "  \"detected_foods\": [\"food1\", \"food2\"],\n"
                            "  \"calories\": 500,\n"
                            "  \"protein_g\": 20.5,\n"
                            "  \"carbs_g\": 60.0,\n"
                            "  \"fat_g\": 10.2,\n"
                            "  \"vitamins\": [\"B1\", \"C\"]\n"
                            "}\n\n"
                            "Respond in valid JSON only. Do not include any text, descriptions or prefixes."
                        )
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Identify the food and give nutritional breakdown in JSON."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=500,
                extra_headers={
                    "HTTP-Referer": "https://your-app.com",
                    "X-Title": "NutriBot"
                }
            )
        except Exception as e:
            st.error(f"❌ API Error: {e}")
            st.stop()

    llm_text = response.choices[0].message.content.strip()
    try:
        # Extract JSON if model wrapped it in extra text
        first_brace = llm_text.find('{')
        last_brace = llm_text.rfind('}') + 1
        if first_brace != -1 and last_brace != -1:
            llm_text = llm_text[first_brace:last_brace]
        data = json.loads(llm_text)
    except json.JSONDecodeError as e:
        st.error("❌ JSON parse error")
        st.code(llm_text)
        st.stop()

    # Safe Extractors
    def safe_get(key, default=""):
        val = data.get(key, default)
        if isinstance(val, list):
            return ", ".join(map(str, val))
        return val if val is not None else default

    def safe_number(key, default=0.0, as_int=False):
        val = data.get(key, default)
        if isinstance(val, list):
            val = val[0] if val else default
        if val is None:
            val = default
        return int(val) if as_int else float(val)

    # Extract data
    detected_foods = safe_get("detected_foods")
    calories = safe_number("calories", 0, as_int=True)
    protein_g = safe_number("protein_g", 0.0)
    carbs_g = safe_number("carbs_g", 0.0)
    fat_g = safe_number("fat_g", 0.0)
    vitamins = safe_get("vitamins")

    # Show Result
    st.success("✅ Detected Nutrition Data:")
    st.markdown(f"**🍽️ Foods:** {detected_foods}")
    st.markdown(f"**🔥 Calories:** {calories} kcal")
    st.markdown(f"**💪 Protein:** {protein_g} g")
    st.markdown(f"**🍞 Carbs:** {carbs_g} g")
    st.markdown(f"**🧈 Fat:** {fat_g} g")
    st.markdown(f"**🧪 Vitamins:** {vitamins}")

    # Timestamp
    ist = pytz.timezone('Asia/Kolkata')
    timestamp_ist = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

    # Save to SQLite
    conn = sqlite3.connect("nutrition_log.db")
    cursor = conn.cursor()
    cursor.execute("""
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

    cursor.execute("""
    INSERT INTO food_nutrition (
        detected_foods, calories, protein_g, carbs_g, fat_g, vitamins, raw_llm_response, timestamp
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        detected_foods, calories, protein_g, carbs_g, fat_g, vitamins, llm_text, timestamp_ist
    ))
    conn.commit()

    df = pd.read_sql("SELECT * FROM food_nutrition ORDER BY id DESC LIMIT 5", conn)
    conn.close()

    st.subheader("📋 Last 5 Entries")
    st.dataframe(df, use_container_width=True)
