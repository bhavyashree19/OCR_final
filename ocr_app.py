import streamlit as st
import requests
from PIL import Image

# Function to perform OCR using OCR.space API
def perform_ocr(image_file):
    api_key = 'K81684211288957'  # Your actual API key
    ocr_url = 'https://api.ocr.space/parse/image'
    
    if image_file is not None:
        files = {'file': image_file}
        headers = {'apikey': api_key}
        response = requests.post(ocr_url, headers=headers, files=files)
        result = response.json()

        if response.status_code == 200 and not result.get('IsErroredOnProcessing', False):
            return result.get('ParsedResults')[0].get('ParsedText', 'No text found')
        else:
            return result.get('ErrorMessage', 'Error during processing')
    
    return 'No image file provided'

# Streamlit app interface
st.title("OCR Space API with Streamlit")

# Upload image file
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")
    st.write("Performing OCR...")
    
    # Call the OCR function and display the result
    extracted_text = perform_ocr(uploaded_file)
    st.text_area("Extracted Text", extracted_text, height=200)
