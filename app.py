# app.py
import streamlit as st
from PIL import Image
from utils.ocr import extract_text_from_image
from utils.translator import translate_text
from utils.nutrition import get_nutrition_info
from db.db_connect import get_db_connection
import pandas as pd

st.title("🍽️ NutriLingo - Translate & Track Nutrition from Menus")

# Initialize session state
if "combined_menu" not in st.session_state:
    st.session_state.combined_menu = []
if "items_to_log" not in st.session_state:
    st.session_state.items_to_log = []
if "selected_ocr_items" not in st.session_state:
    st.session_state.selected_ocr_items = []

uploaded_file = st.file_uploader("Upload a menu image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Menu", use_column_width=True)

    with st.spinner("Extracting text using EasyOCR..."):
        menu_items = extract_text_from_image(image)

    st.subheader("Extracted Menu Items:")
    for i, item in enumerate(menu_items, start=1):
        st.markdown(f"**{i}.** {item}")

    if menu_items:
        col1, col2 = st.columns(2)

        with col1:
            # 🄤 Language selection + Translate button
            target_language = st.selectbox(
                "Select target language for translation:",
                ["en", "fr", "es", "de", "hi", "zh", "ja", "it"],
                index=0
            )
            if st.button("🄤 Translate Menu"):
                joined_text = "\n".join(menu_items)
                with st.spinner(f"Translating to {target_language.upper()}..."):
                    translated_items = translate_text(joined_text, target_language)

                if len(menu_items) == len(translated_items):
                    st.session_state.combined_menu = list(zip(menu_items, translated_items))
                else:
                    st.warning("Mismatch in translation count.")
                    st.session_state.combined_menu = [(item, "") for item in menu_items]

        with col2:
            st.markdown("🍴 **Select Items from OCR to Get Nutrition Info**")
            selected_ocr_items = st.multiselect("Choose items:", menu_items)

            if selected_ocr_items:
                st.session_state.selected_ocr_items = selected_ocr_items
                st.subheader("🥗 Nutrition Info")
                st.session_state.items_to_log = []

                for item in selected_ocr_items:
                    info = get_nutrition_info(item)
                    if "error" in info:
                        st.error(f"{item} → Error fetching data: {info['error']}")
                    else:
                        st.markdown(f"""
                        **{info['match_name']}** {f"({info.get('source')})" if info.get('source') else ''}
                        - Calories: {info['calories']} kcal  
                        - Protein: {info['protein']} g  
                        - Carbs: {info['carbs']} g  
                        - Fat: {info['fat']} g
                        ---""")
                        st.session_state.items_to_log.append({
                            "item_name": info["match_name"],
                            "calories": info["calories"]
                        })

                if st.button("📅 Add to Today's Calorie Log"):
                    conn = get_db_connection()
                    if conn:
                        try:
                            cursor = conn.cursor()
                            for entry in st.session_state.items_to_log:
                                cursor.execute("""
                                    INSERT INTO food_log (user_id, item_id, date_logged)
                                    SELECT u.user_id, mi.item_id, CURRENT_DATE
                                    FROM users u
                                    JOIN menu_items mi ON LOWER(mi.item_text_translated) = LOWER(%s)
                                    WHERE u.user_id = 1
                                """, (entry["item_name"],))
                                # ✅ Insert into nutrition if not already present
                                cursor.execute("""
                                    INSERT INTO nutrition (item_id, calories, protein, carbs, fat)
                                    SELECT mi.item_id, %s, %s, %s, %s
                                    FROM menu_items mi
                                    WHERE LOWER(mi.item_text_translated) = LOWER(%s)
                                    ON CONFLICT (item_id) DO NOTHING;
                                """, (entry["calories"], 0, 0, 0, entry["item_name"]))
                            conn.commit()
                            st.success("✅ Items logged for today.")
                        except Exception as e:
                            st.error(f"❌ Failed to log: {e}")
                        finally:
                            conn.close()
                    st.session_state.items_to_log = []

                if st.button("🔄 Clear Selection and Reselect"):
                    st.session_state.selected_ocr_items = []
                    st.experimental_rerun()

                if st.button("📈 Show Today's Calorie Intake"):
                    conn = get_db_connection()
                    if conn:
                        try:
                            cursor = conn.cursor()
                            cursor.execute("""
                                SELECT SUM(n.calories)
                                FROM food_log f
                                JOIN menu_items mi ON f.item_id = mi.item_id
                                JOIN nutrition n ON n.item_id = mi.item_id
                                WHERE f.user_id = 1 AND f.date_logged = CURRENT_DATE
                            """)
                            total = cursor.fetchone()[0] or 0
                            st.info(f"🧶 Calories consumed today: **{total} kcal**")
                        except Exception as e:
                            st.error(f"❌ Error fetching total: {e}")
                        finally:
                            conn.close()

    # 📜 Show translated menu if available
    if st.session_state.combined_menu:
        st.subheader("📜 Side-by-Side Translated Menu:")
        for orig, trans in st.session_state.combined_menu:
            st.markdown(f"**{orig}**  →  *{trans}*")

        st.subheader("🍛 Select Translated Dish for Nutrition:")
        dish_options = [trans for _, trans in st.session_state.combined_menu]
        selected_dish = st.selectbox("Choose a translated item:", dish_options)

        invalid_terms = ["FOOD MENU", "MENU", "BREAKFAST", "DINNER", "LUNCH"]

        if st.button("🔬 Get Nutrition Info for Translated Item"):
            if selected_dish.strip().upper() in invalid_terms:
                st.error("⚠️ Please select a valid food item, not a menu header.")
            else:
                with st.spinner(f"Fetching nutrition info for {selected_dish}..."):
                    info = get_nutrition_info(selected_dish)

                if "error" in info:
                    st.error(f"{selected_dish} → Error fetching data: {info['error']}")
                else:
                    st.success("✅ Nutrition Info:")
                    st.markdown(f"""
                    **{selected_dish}**
                    - Calories: {info['calories']} kcal  
                    - Protein: {info['protein']} g  
                    - Carbs: {info['carbs']} g  
                    - Fat: {info['fat']} g
                    """)
