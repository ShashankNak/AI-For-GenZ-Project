import streamlit as st
from pathlib import Path


def storeSession(uploaded_file, chatbot):
    if "docs" not in st.session_state:
        st.session_state["docs"] = []

    doc = st.session_state.get("docs",[])
    doc.append(uploaded_file)
    st.session_state["docs"] = doc

    if "chatbot" in st.session_state:
        del st.session_state["chatbot"]
    st.session_state["chatbot"] = chatbot

st.title("Train Bot")

chatbot = st.session_state.get("chatbot", None)

if chatbot is not None and chatbot.initialized:
    st.subheader("Drag & Drop any file (format: pdf, docx, txt, json)")
    uploaded_file = st.file_uploader(
        "Upload Docs", type=["pdf", "docx", "txt", "json", "csv","xlsx"]
    )
    if st.button("Process", key="process"):
        if uploaded_file is not None:
            file_details = {
                "FileName": uploaded_file.name,
                "FileType": uploaded_file.type,
                "FileSize": uploaded_file.size,
            }
            st.write(file_details)

            # Save uploaded file to 'F:/tmp' folder.
            save_folder = 'savedDocs/'
            save_path = Path(save_folder, uploaded_file.name)
            with open(str(save_path), 'wb') as w:
                w.write(uploaded_file.getvalue())

            file_types = {
                "application/pdf": ("pdf", "PDF"),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ("docx", "Docx"),
                "text/plain": ("txt", "Text"),
                "application/json": ("json", "JSON"),
                "text/csv": ("csv", "CSV"),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ("xlsx", "XLSX"),
            }

            file_type = uploaded_file.type
            if file_type in file_types:
                extension, file_format = file_types[file_type]
                method = getattr(chatbot, f"{extension}_data", None)
                if callable(method):
                    method = getattr(chatbot, f"{extension}_data")
                    method(uploaded_file)
                else:
                    st.error(f"Chatbot does not support {file_format} files.")
                storeSession(uploaded_file, chatbot)
                st.success(f"{file_format} file processed successfully")
                st.write("You can chat now!")
            

else:
    st.error("Please add API Key first!")


