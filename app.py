import streamlit as st
import fitz
import google.generativeai as genai

st.set_page_config(page_title="AI Study Assistant", page_icon="📚")
st.title("📚 AI Study Assistant")
st.caption("Upload any PDF and ask questions instantly — Built by Ankur Tiwari")

api_key = st.text_input("Paste your Gemini API Key", type="password")
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file and api_key:
    with st.spinner("Reading your document..."):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "".join([page.get_text() for page in doc])
    st.success("Document ready! Ask your question below.")
    question = st.text_input("Type your question:")
    if question:
        with st.spinner("Thinking..."):
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-pro")
            prompt = f"""You are a helpful study assistant.
Use ONLY the document content below to answer the question.
If answer not found say: I could not find this in the document.
Document:
{text[:10000]}
Question: {question}"""
            response = model.generate_content(prompt)
        st.markdown(f"**Answer:** {response.text}")
