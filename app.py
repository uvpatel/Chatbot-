import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
import io
import PyPDF2
import docx

# Configure Gemini API
genai.configure(api_key="AIzaSyB2ijlVpMEvbENDTYf4VLkykPuMijPwG04")
model = genai.GenerativeModel("gemini-1.5-flash")

# Image to inline data
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
        text += page.extract_text()
    return text

# Extract text from DOCX
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Streamlit UI
st.set_page_config(page_title="Gemini Chatbot with Image & File Support", layout="centered")
st.title("🤖 Gemini Chatbot")
st.markdown("Ask anything using text, images, or upload a file (PDF, DOCX, etc.)")

chat_mode = st.radio("Choose input mode:", ["Text", "Image", "File"])

if chat_mode == "Text":
    text_input = st.text_input("💬 Enter your question:")
    if st.button("Ask"):
        if text_input.strip():
            with st.spinner("Generating response..."):
                try:
                    response = model.generate_content(text_input)
                    st.success(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a question.")

elif chat_mode == "Image":
    uploaded_image = st.file_uploader("📤 Upload an image", type=["png", "jpg", "jpeg"])
    image_prompt = st.text_input("🧠 What do you want to ask about this image?")
    if uploaded_image and image_prompt.strip():
        if st.button("Analyze Image"):
            with st.spinner("Analyzing image..."):
                try:
                    image_part = get_image_parts(uploaded_image)
                    response = model.generate_content(
                        contents=[{"role": "user", "parts": [image_prompt, image_part]}]
                    )
                    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
                    st.success(response.text)
                except Exception as e:
                    st.error(f"Failed to analyze image: {e}")
    elif uploaded_image:
        st.warning("Please enter a question about the image.")

elif chat_mode == "File":
    uploaded_file = st.file_uploader("📄 Upload a file", type=["pdf", "txt", "docx"])
    file_prompt = st.text_input("🧠 What do you want to ask about this file?")
    if uploaded_file and file_prompt.strip():
        if st.button("Analyze File"):
            with st.spinner("Reading and analyzing file..."):
                try:
                    file_text = ""
                    if uploaded_file.type == "application/pdf":
                        file_text = extract_text_from_pdf(uploaded_file)
                    elif uploaded_file.type == "text/plain":
                        file_text = uploaded_file.read().decode("utf-8")
                    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        file_text = extract_text_from_docx(uploaded_file)

                    full_prompt = f"{file_prompt}\n\nContent:\n{file_text}"
                    response = model.generate_content(full_prompt)
                    st.success(response.text)
                except Exception as e:
                    st.error(f"Failed to analyze file: {e}")
    elif uploaded_file:
        st.warning("Please enter a question about the file.")
