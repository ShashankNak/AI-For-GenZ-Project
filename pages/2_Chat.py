import streamlit as st

st.title("DocumentAI")

chatbot = st.session_state.get("chatbot", None)

if chatbot is not None and (chatbot.pdfTrained or chatbot.docxTrained or chatbot.textTrained or chatbot.csvTrained or chatbot.jsonTrained or chatbot.excelTrained):
    st.subheader("Your model is Trained on the following files: ")
    if "docs" in st.session_state:
        doc = st.session_state.get("docs",[])
        for d in doc:
            st.write(d.name)


    ask = st.text_input("Enter your query: ", key="query")
    if st.button("Ask", key="ask") and ask.strip() != "":
        response = chatbot.chat_with_docs(ask)
        st.write(response)
else:
    st.error("Please add a Document first!")