# 🥗 NutriLingo

**NutriLingo** is a GenAI-powered web application that extracts text from food menus using OCR, translates it into English, fetches nutritional information using the Spoonacular API, and helps users track their daily calorie intake — all within a sleek Streamlit dashboard and backed by PostgreSQL.

## 🚀 Features

🔍 **OCR-Based Menu Extraction**  
Upload images of menus (in any language), and the app automatically extracts menu items using Tesseract OCR.

🌐 **AI-Powered Translation**  
Utilizes GPT-4 (or Google Translate API) to convert menu text into English, allowing for international use cases.

🥦 **Nutritional Information via Spoonacular API**  
Auto-fetches calories, protein, fat, and carb content of dishes using AI-extracted and translated dish names.

📊 **Calorie Tracker Dashboard**  
Users can log meals and view daily nutritional intake over time with interactive visualizations.

🗄️ **PostgreSQL Integration**  
All extracted, translated, and nutrition data — along with calorie tracking — is stored in a PostgreSQL database for persistent and structured access.

---

## 🧱 Tech Stack

| Component | Technology |
|----------|-------------|
| Frontend | Streamlit |
| Backend | Python |
| OCR | Tesseract / EasyOCR |
| Translation | GPT-4 / Google Translate API |
| Nutrition Data | [Spoonacular API](https://spoonacular.com/food-api) |
| Database | PostgreSQL (via SQLAlchemy/psycopg2) |
| Hosting | Streamlit Cloud / AWS EC2 (optional) |

---

## 🗂️ Project Structure
nutrilingo/
├── app.py                          # Main Streamlit app entry point
├── config.py                       # Configuration (API keys, DB config)
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (not tracked)
├── README.md                       # Project documentation

├── ocr/                            # OCR module
│   ├── __init__.py
│   └── ocr_utils.py                # Tesseract / EasyOCR logic

├── translation/                    # Translation module
│   ├── __init__.py
│   └── translation_utils.py        # GPT-4 / Google Translate logic

├── nutrition/                      # Nutrition info module
│   ├── __init__.py
│   └── nutrition_api.py            # Spoonacular API integration

├── db/                             # PostgreSQL schema & database logic
│   ├── __init__.py
│   ├── models.py                   # SQLAlchemy models
│   ├── db_manager.py               # DB connection + query helpers
│   └── schema.sql                  # SQL schema if needed for manual setup

├── dashboard/                      # Dashboard visualizations
│   ├── __init__.py
│   └── analytics.py                # Calorie graphs, user history, etc.

├── assets/                         # Static assets (images, icons)
│   └── logo.png

└── utils/                          # Misc utilities (formatting, helpers)
    ├── __init__.py
    └── helpers.py

---
## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/nutrilingo.git
cd nutrilingo

pip install -r requirements.txt
```

---

## ✅ Use Cases

- **Tourists & Travelers**: Struggling to read a menu in a foreign language? NutriLingo makes it easy to translate and understand what you’re about to eat — including the calories.
- **Fitness Enthusiasts**: Log your meals, track calories, and visualize your daily intake.
- **Dieticians & Nutritionists**: Use the app to analyze local menus for clients and give better food recommendations.
- **Health-Conscious Users**: Keep a record of nutritional content while eating out or ordering food.

---

## 🔭 Future Scope

- 🔐 **User Authentication** for personalized dashboards and history
- 🗣️ **Voice-to-Text Meal Logging**
- 📈 **Weekly and Monthly Nutrition Reports**
- 🍽️ **AI-Based Meal Recommendations**
- 📲 **Mobile App Version with Camera Integration**
- ☁️ **Cloud Storage & Analysis of User Food Logs**
- 🧠 **Personalized AI Assistant for Dietary Planning**

---

## 💡 Inspiration

The idea was inspired by the common struggle of understanding **foreign language menus**, especially when traveling or dining at ethnic restaurants. NutriLingo aims to bridge the language barrier while promoting health-conscious decisions using **GenAI, OCR, NLP**, and **data-driven nutrition insights** — all in one seamless app.

---

## 🙌 Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Google Translate API](https://cloud.google.com/translate)
- [OpenAI GPT-4](https://openai.com/)
- [Spoonacular API](https://spoonacular.com/food-api)
- [Streamlit](https://streamlit.io/)
- [PostgreSQL](https://www.postgresql.org/)

---

## 📬 Contact

👨‍💻 **Amrut Prasad Kulkarni**  
📧 amrutkulk11@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/amrutkulkarni11)  
🔗 [GitHub](https://github.com/amrutkulkarni11)

---

## ⭐️ Show Your Support

If you found this project useful or inspiring:

- ⭐️ Star this repo
- 🌀 Fork it for your own use
- 🗣️ Share it with your friends or developer community
- 📧 Feel free to connect and collaborate!

---

 
