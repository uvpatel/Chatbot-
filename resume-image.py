from pdf2image import convert_from_bytes

# Convert PDF to list of images
def convert_pdf_to_images(pdf_file):
    images = convert_from_bytes(pdf_file.read())
    return images

# Process fallback image if text extraction fails
def analyze_resume_as_images(images, prompt):
    responses = []
    for img in images:
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        image_bytes = buffered.getvalue()

        image_part = {
            "inline_data": {
                "mime_type": "image/png",
                "data": base64.b64encode(image_bytes).decode("utf-8"),
            }
        }

        response = model.generate_content(
            contents=[{"role": "user", "parts": [prompt, image_part]}]
        )
        responses.append(response.text)

    return "\n\n".join(responses)
