import streamlit as st
from model import ChatBot

chatbot = ChatBot()



st.set_page_config(
    page_title="DocumentAI",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Document Bot")

st.write("Steps to use Document Bot: ")
st.write("1. Add API Key")
st.write("2. Train Bot on Documents")
st.write("3. Chat with Bot")


api = st.text_input("API_KEY", key="api_key_input")
if st.button("Add API Key",key="add_api_key"):
    if api.strip() != "":
        chatbot.initializeKey(api)
        if chatbot.initialized:
            st.success("API Key added successfully!")
            if "chatbot" in st.session_state:
                del st.session_state["chatbot"]
            st.session_state['chatbot'] = chatbot
            st.write("You can add Docs now!")
        else:
            st.error("Failed to add API Key")

