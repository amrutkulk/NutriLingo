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
        # Now returns a list of lines (menu items)
        menu_items = extract_text_from_image(image)

    # Display items as a numbered list
    st.subheader("Extracted Menu Items:")
    for i, item in enumerate(menu_items, start=1):
        st.markdown(f"**{i}.** {item}")

    if menu_items:
        # Language selector
        target_language = st.selectbox(
            "Select target language",
            ["en", "fr", "es", "de", "hi", "zh", "ja", "it"],
            index=0
        )

        # Join menu items into one block of text for translation
        joined_text = "\n".join(menu_items)

        with st.spinner(f"Translating to {target_language.upper()}..."):
            translated_items = translate_text(joined_text, target_language)

        st.subheader("📝 Side-by-Side Translated Menu:")

        # Ensure list lengths match before pairing
        if len(menu_items) == len(translated_items):
            for original, translated in zip(menu_items, translated_items):
                st.markdown(f"**{original}**  →  *{translated}*")
        else:
            st.warning("Mismatch in translation count. Showing raw translated block instead.")
            st.text_area("Translated Text", value="\n".join(translated_items), height=200)
