import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
import io
import PyPDF2
import docx

# Configure Gemini API
genai.configure(api_key="AIzaSyB2ijlVpMEvbENDTYf4VLkykPuMijPwG04")  # Replace with your key
model = genai.GenerativeModel("gemini-1.5-flash")

# Convert image to inline_data
def get_image_parts(uploaded_file):
    image = Image.open(uploaded_file)
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_bytes = buffered.getvalue()
    return {
        "inline_data": {
            "mime_type": "image/png",
            "data": base64.b64encode(image_bytes).decode("utf-8"),
        }
    }

# Extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Extract text from DOCX
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Streamlit UI
st.set_page_config(page_title="Resume Analyzer - Gemini Chatbot", layout="centered")
st.title("📄 Gemini Resume Analyzer")
st.markdown("Upload a **resume** in PDF, DOCX, or image format and get instant feedback, insights, or improvements!")

chat_mode = st.radio("Choose input type:", ["Text", "Resume (File)", "Resume (Image)"])

# TEXT MODE
if chat_mode == "Text":
    text_input = st.text_input("💬 Ask your question:")
    if st.button("Ask Gemini"):
        if text_input.strip():
            with st.spinner("Gemini is thinking..."):
                try:
                    response = model.generate_content(text_input)
                    st.success(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a question.")

# FILE MODE: Resume as DOCX, PDF, or TXT
elif chat_mode == "Resume (File)":
    uploaded_file = st.file_uploader("📤 Upload your resume", type=["pdf", "txt", "docx"])
    file_prompt = st.text_input("🧠 What do you want to know about your resume? (e.g., Improve this resume for a Data Analyst role)")

    if uploaded_file and file_prompt.strip():
        if st.button("Analyze Resume"):
            with st.spinner("Analyzing your resume..."):
                try:
                    file_text = ""
                    if uploaded_file.type == "application/pdf":
                        file_text = extract_text_from_pdf(uploaded_file)
                    elif uploaded_file.type == "text/plain":
                        file_text = uploaded_file.read().decode("utf-8")
                    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        file_text = extract_text_from_docx(uploaded_file)

                    if file_text.strip() == "":
                        st.warning("Resume appears to be image-based. Try uploading as an image instead.")
                    else:
                        full_prompt = f"{file_prompt}\n\nResume Content:\n{file_text}"
                        response = model.generate_content(full_prompt)
                        st.success(response.text)
                except Exception as e:
                    st.error(f"Failed to analyze resume: {e}")
    elif uploaded_file:
        st.warning("Please enter a question to analyze your resume.")

# IMAGE MODE: Resume as PNG/JPG
elif chat_mode == "Resume (Image)":
    uploaded_image = st.file_uploader("📤 Upload an image of your resume", type=["png", "jpg", "jpeg"])
    image_prompt = st.text_input("🧠 What do you want to know about this resume image?")

    if uploaded_image and image_prompt.strip():
        if st.button("Analyze Resume Image"):
            with st.spinner("Reading resume from image..."):
                try:
                    image_part = get_image_parts(uploaded_image)
                    response = model.generate_content(
                        contents=[{"role": "user", "parts": [image_prompt, image_part]}]
                    )
                    st.image(uploaded_image, caption="Uploaded Resume", use_column_width=True)
                    st.success(response.text)
                except Exception as e:
                    st.error(f"Failed to analyze image: {e}")
    elif uploaded_image:
        st.warning("Please describe what you want to ask about the image.")

