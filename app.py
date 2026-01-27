# app.py
import streamlit as st
from budget_chatbot import ask_budget_chatbot

# Set page config
st.set_page_config(
    page_title="Nepal Budget Chatbot",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Nepal Budget Chatbot Assistant")
st.markdown(
    """
यो च्याटबोटले तपाईंको प्रश्न अनुसार नेपाल सरकारको बजेट 2082/2083 का तथ्यांक र कार्यक्रमहरूको आधारमा जवाफ दिन्छ।  
कृपया नेपाली भाषामा आफ्नो प्रश्न टाइप गर्नुहोस्।
"""
)

# User input
query = st.text_input("Question realted to Budget:", "")

# Submit button
if st.button("Submit"):
    if query.strip() == "":
        st.warning("कृपया पहिले प्रश्न लेख्नुहोस्।")
    else:
        with st.spinner("बजेट कागजात अनुसार उत्तर खोज्दै..."):
            answer = ask_budget_chatbot(query)
        st.subheader("उत्तर:")
        st.write(answer)
