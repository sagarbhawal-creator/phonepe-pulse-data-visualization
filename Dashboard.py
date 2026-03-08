import streamlit as st

st.set_page_config(
    page_title="PhonePe Transaction Analysis",
    layout="wide"
)

st.title("📊 PhonePe Transaction Analysis Dashboard")

st.divider()

st.header("📌 Project Overview")

st.write("""
This project analyzes **PhonePe digital payment data** across India.
The dashboard provides insights into transaction growth, device usage,
insurance adoption, and regional market expansion.

Using interactive visualizations, users can explore the trends
across **states, districts, years, and quarters**.
""")

st.divider()

st.header("🛠 Tools Used")

st.write("""
• Python  
• SQL (MySQL)  
• Streamlit  
• Pandas  
• Plotly  
• GitHub Dataset
""")

st.divider()

st.header("🎯 Objectives")

st.write("""
• Analyze transaction trends over the years  
• Identify top performing states and districts  
• Study device brand dominance among users  
• Analyze insurance adoption trends  
• Understand market expansion across regions
""")

st.divider()

st.header("👨‍💻 Developed By")

st.write("**Sagar Bhawal**")

st.info("Use the sidebar to navigate to the **Analysis Dashboard**.")