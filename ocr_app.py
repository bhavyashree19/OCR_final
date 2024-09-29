import streamlit as st
import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def load_css(file_name):
    """Load CSS file."""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def assess_image_quality(img):
    if img is None or img.size[0] < 100 or img.size[1] < 100:
        logging.error("Image quality is poor.")
        return False
    if img.mode not in ["RGB", "L"]:
        logging.error("Unsupported image mode.")
        return False
    return True

def preprocess_image(img):
    img = img.convert('L')
    img = img.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    img = img.filter(ImageFilter.MedianFilter(size=3))
    img = img.point(lambda p: p > 128 and 255)
    return img

def perform_ocr(img):
    try:
        return pytesseract.image_to_string(img, lang='eng+hin')
    except pytesseract.pytesseract.TesseractError as e:
        logging.error(f"OCR error: {e}")
        return None

def highlight_keywords(text, keywords):
    for keyword in keywords:
        text = text.replace(keyword, f"<mark>{keyword}</mark>")
    return text

def main():
    load_css('styles.css')  # Load CSS file

    st.title("OCR Text Extractor from Image Upload")
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        if not assess_image_quality(img):
            st.error("Image quality is poor.")
            return
        
        img = preprocess_image(img)
        extracted_text = perform_ocr(img)
        final_text = extracted_text.strip() if extracted_text else ""
        
        logging.info("Extracted Text:")
        logging.info(final_text)
        st.subheader("Extracted Text:")
        st.text(final_text)

        keywords = st.text_input("Enter keywords to search within the extracted text (comma-separated):")
        if keywords:
            keyword_list = [k.strip() for k in keywords.split(",")]
            highlighted_text = highlight_keywords(final_text, keyword_list)
            st.markdown("### Search Results:")
            st.markdown(highlighted_text, unsafe_allow_html=True)

        output_filename = 'extracted_text.txt'
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(final_text)
        st.success(f"Text saved to '{output_filename}'")

if __name__ == "__main__":
    main()
