# app.py
import streamlit as st
from PIL import Image
from utils.ocr import extract_text_from_image
from utils.translator import translate_text
from db.db_connect import get_db_connection

st.title("🍽️ NutriLingo - Translate & Track Nutrition from Menus")

uploaded_file = st.file_uploader("Upload a menu image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Menu", use_column_width=True)

    with st.spinner("Extracting text using EasyOCR..."):
        extracted_text = extract_text_from_image(image)

    st.text_area("Extracted Text", value=extracted_text, height=200)

    if extracted_text:
        with st.spinner("Translating text..."):
            translated_text = translate_text(extracted_text)
        st.text_area("Translated Text", value=translated_text, height=200)
