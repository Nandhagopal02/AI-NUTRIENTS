import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import altair as alt

# ----------------- Page Setup -----------------
st.set_page_config(
    page_title="📊 AI Nutrition Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Fetch Data from MySQL -----------------
@st.cache_data
def get_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",             # 🔁 Your DB username
        password="root",         # 🔁 Your DB password
        database="fp"            # 🔁 Your DB name
    )
    query = "SELECT * FROM FitnessNutrition ORDER BY timestamp DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = get_data()

# ----------------- Title -----------------
st.title("📊 Smartest AI Nutrition Dashboard")
st.markdown("Get insights into your food and fitness data.")

# ----------------- Top Metrics -----------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("🔥 Total Calories", f"{df['calories'].sum()} kcal")
col2.metric("💪 Protein", f"{df['protein_g'].sum()} g")
col3.metric("🍞 Carbs", f"{df['carbs_g'].sum()} g")
col4.metric("🧈 Fat", f"{df['fat_g'].sum()} g")

st.markdown("---")

# ----------------- Calories Burned -----------------
st.subheader("🏋️ Calories Burned by Exercise")
exercise_cals = {
    "Pull-ups": df["pull_up_calories"].sum(),
    "Push-ups": df["push_up_calories"].sum()
}
bar_data = pd.DataFrame({
    "Exercise": list(exercise_cals.keys()),
    "Calories": list(exercise_cals.values())
})
fig_bar = px.bar(
    bar_data,
    x="Exercise",
    y="Calories",
    color="Exercise",
    title="Calories Burned – Pull-ups vs Push-ups",
    color_discrete_sequence=["#1f77b4", "#ff7f0e"]
)
st.plotly_chart(fig_bar, use_container_width=True)

# ----------------- Top Foods Pie Chart -----------------
st.subheader("🍽️ Top 5 Detected Foods")
top_foods = df['detected_foods'].dropna().value_counts().head(5)
fig_foods = px.pie(
    names=top_foods.index,
    values=top_foods.values,
    title="Top 5 Foods",
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.RdBu
)
fig_foods.update_traces(textinfo='label+percent')
st.plotly_chart(fig_foods, use_container_width=True)

# ----------------- Nutrient Trend Over Time -----------------
st.subheader("📈 Nutrient Trends Over Time")
nutrient = st.selectbox("Select a nutrient:", ["calories", "protein_g", "carbs_g", "fat_g"])
line_chart = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X('timestamp:T', title='Date'),
    y=alt.Y(nutrient, title=nutrient.capitalize()),
    tooltip=['timestamp', nutrient]
).properties(
    title=f"{nutrient.capitalize()} Over Time",
    height=400
).interactive()
st.altair_chart(line_chart, use_container_width=True)

# ----------------- Footer -----------------
st.markdown("---")
st.caption(f"📅 Last updated: {df['timestamp'].max().strftime('%Y-%m-%d %H:%M')}")
st.caption("© 2025 Smartest AI Nutrition")
