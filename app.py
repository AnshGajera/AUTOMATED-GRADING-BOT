# app.py
import streamlit as st
import os
import tempfile
from utils import extract_text_from_pdf, extract_text_from_docx
from main import run_grading_pipeline

st.set_page_config(page_title="AI Assignment Grader", page_icon="🧠", layout="centered")

st.markdown("## 📚 AI Assignment Grading Assistant")
st.markdown("Upload a student's assignment in PDF or DOCX format. The AI will read, grade, and provide feedback.")

uploaded_file = st.file_uploader("📤 Upload Assignment File", type=["pdf", "docx"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        file_path = tmp_file.name

    # Extract assignment text
    if uploaded_file.name.endswith(".pdf"):
        assignment_text = extract_text_from_pdf(file_path)
    elif uploaded_file.name.endswith(".docx"):
        assignment_text = extract_text_from_docx(file_path)
    else:
        st.error("Unsupported file type!")
        st.stop()

    st.markdown("### 📄 Extracted Text")
    st.text_area("Assignment Preview", value=assignment_text, height=300)

    if st.button("📝 Grade Assignment"):
        with st.spinner("Grading in progress..."):
            result = run_grading_pipeline(assignment_text)

        st.success("🎓 Grading Complete")
        st.markdown("### 📊 Grade & Score")
        st.json(result)

        # Optional: Save to CSV or send email (not shown in UI)
