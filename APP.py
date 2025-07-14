import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AI Nutrition Assistant",
    page_icon="🥗",
    layout="wide"
)

# Top Banner with Columns
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3172/3172880.png", width=120)
with col2:
    st.markdown("""
    <h1 style='font-size: 36px; color: #4CAF50;'>Smartest AI Nutrition Assistant 🥗</h1>
    <p style='font-size: 18px;'>Your AI-powered wellness guide for food, fitness and health insights.</p>
    """, unsafe_allow_html=True)

# Divider
st.markdown("---")

# Highlights Section
st.markdown("## 🌟 What You Can Do")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    - 📸 **Upload Meals** to get calorie and nutrition breakdown  
    - 🧠 **Chat with AI** about food, macros, and healthy eating  
    - 🏃 **Track Exercises** with automatic rep counting and calories  
    """)

with col2:
    st.markdown("""
    - 📊 **Visual Dashboards** to view your fitness journey  
    - 📅 **Daily Summaries** for yesterday's nutrition & exercise  
    - ☁️ **Cloud-Hosted**, use from anywhere with a browser  
    """)

# Call to Action
st.success("👉 Use the sidebar to begin your health journey today!")

# Footer or Branding
st.markdown("---")
st.caption("© 2025 Smartest AI Nutrition • Built with ❤️ using Streamlit")
