import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import pytz

# Page setup
st.set_page_config(page_title="📅 Daily Summary", layout="wide")
st.title("📊 Yesterday's Nutrition & Exercise Summary")

# Get yesterday's date in IST
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)
yesterday = (now - timedelta(days=1)).date()

# --- Load FOOD DATA ---
conn_food = sqlite3.connect("nutrition_log.db")
df_food = pd.read_sql_query("SELECT * FROM food_nutrition", conn_food)
conn_food.close()

df_food['timestamp'] = pd.to_datetime(df_food['timestamp'])
df_food_yesterday = df_food[df_food['timestamp'].dt.date == yesterday]

# --- Load EXERCISE DATA ---
conn_ex = sqlite3.connect("exercise_log.db")
df_ex = pd.read_sql_query("SELECT * FROM exercise_log", conn_ex)
conn_ex.close()

df_ex['timestamp'] = pd.to_datetime(df_ex['timestamp'])
df_ex_yesterday = df_ex[df_ex['timestamp'].dt.date == yesterday]

# --- Summarize NUTRITION ---
total_calories_in = df_food_yesterday['calories'].sum()
total_protein = df_food_yesterday['protein_g'].sum()
total_carbs = df_food_yesterday['carbs_g'].sum()
total_fat = df_food_yesterday['fat_g'].sum()

# --- Summarize EXERCISE ---
total_calories_burned = df_ex_yesterday['calories_burned'].sum()

# --- Display Metrics ---
st.header(f"🗓️ Summary for {yesterday.strftime('%A, %d %B %Y')}")

col1, col2 = st.columns(2)
with col1:
    st.subheader("🍱 Nutrition Intake")
    st.metric("🔥 Calories In", f"{total_calories_in} kcal")
    st.metric("💪 Protein", f"{round(total_protein, 2)} g")
    st.metric("🍞 Carbs", f"{round(total_carbs, 2)} g")
    st.metric("🧈 Fat", f"{round(total_fat, 2)} g")

with col2:
    st.subheader("🏋️ Exercise Output")
    st.metric("🔥 Calories Burned", f"{round(total_calories_burned, 2)} kcal")
    st.write("✅ Stay active and consistent!")

# --- Expandable Logs ---
st.markdown("---")
with st.expander("🔍 See Detailed Logs for Yesterday"):
    st.markdown("#### 🍱 Food Log")
    st.dataframe(df_food_yesterday, use_container_width=True)
    st.markdown("#### 🏋️ Exercise Log")
    st.dataframe(df_ex_yesterday, use_container_width=True)