import os
import re
import pandas as pd
import requests
from difflib import get_close_matches
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load CSV data globally
try:
    df = pd.read_csv("restaurant_sample.csv")
    df["item_name"] = df["item_name"].astype(str).str.lower()
except FileNotFoundError:
    print("❌ restaurant_sample.csv not found.")
    df = pd.DataFrame(columns=["item_name", "nf_calories", "nf_protein", "nf_total_carbohydrate", "nf_total_fat"])

# Hardcoded fallback nutrition values
hardcoded_nutrition = {
    "cheeseburger": {"calories": 340, "protein": 25, "carbs": 29, "fat": 18},
    "cheese sandwich": {"calories": 310, "protein": 15, "carbs": 33, "fat": 14},
    "chicken burgers": {"calories": 330, "protein": 28, "carbs": 27, "fat": 16},
    "spicy chicken": {"calories": 280, "protein": 26, "carbs": 24, "fat": 12},
    "hot dog": {"calories": 290, "protein": 11, "carbs": 27, "fat": 20},
    "fruit salad": {"calories": 150, "protein": 2, "carbs": 38, "fat": 0.5},
    "cocktails": {"calories": 210, "protein": 0, "carbs": 28, "fat": 0},
    "nuggets": {"calories": 250, "protein": 14, "carbs": 15, "fat": 15},
    "sandwich": {"calories": 220, "protein": 12, "carbs": 25, "fat": 8},
    "french fries": {"calories": 320, "protein": 3, "carbs": 42, "fat": 17},
    "milk shake": {"calories": 330, "protein": 8, "carbs": 45, "fat": 12},
    "iced": {"calories": 90, "protein": 0, "carbs": 23, "fat": 0},
    "orange juice": {"calories": 110, "protein": 2, "carbs": 26, "fat": 0},
    "lemon tea": {"calories": 70, "protein": 0, "carbs": 19, "fat": 0},
    "coffee": {"calories": 5, "protein": 0, "carbs": 1, "fat": 0},
    "tea": {"calories": 2, "protein": 0, "carbs": 1, "fat": 0}
}

# Helper: Clean dish name for fuzzy matching
def clean_dish_name(name: str) -> str:
    # Remove numbers, prices, and symbols like "$34" or "5"
    cleaned = re.sub(r"[$]?\d+(\.\d+)?", "", name)
    return cleaned.strip().lower()

# Helper: Call FatSecret API
def get_fatsecret_data(query: str) -> dict:
    try:
        client_id = os.getenv("FATSECRET_CLIENT_ID")
        client_secret = os.getenv("FATSECRET_CLIENT_SECRET")
        token_url = "https://oauth.fatsecret.com/connect/token"
        food_search_url = "https://platform.fatsecret.com/rest/server.api"

        # Step 1: Get Access Token
        token_response = requests.post(
            token_url,
            data={"grant_type": "client_credentials", "scope": "basic"},
            auth=(client_id, client_secret),
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            raise Exception("No access token received")

        # Step 2: Search for food item
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {
            "method": "foods.search",
            "search_expression": query,
            "format": "json",
        }
        response = requests.get(food_search_url, headers=headers, params=params)
        data = response.json()

        # Step 3: Parse first result
        food = data.get("foods", {}).get("food", [])[0]
        return {
            "name": food.get("food_name"),
            "calories": float(food.get("food_description", "").split("cal")[0].strip()) if "cal" in food.get("food_description", "") else 0,
            "protein": 0,  # FatSecret free tier doesn't return these
            "carbs": 0,
            "fat": 0,
        }

    except Exception as e:
        print(f"❌ FatSecret API error: {e}")
        return None

# Unified nutrition info fetcher
def get_nutrition_info(dish_name: str) -> dict:
    original = dish_name.strip()
    query = clean_dish_name(original)

    # 1. Try CSV dataset
    matches = get_close_matches(query, df["item_name"], n=1, cutoff=0.6)
    if matches:
        match = matches[0]
        result = df[df["item_name"] == match].iloc[0]
        return {
            "match_name": result["item_name"].title(),
            "calories": float(result.get("nf_calories", 0)),
            "protein": float(result.get("nf_protein", 0)),
            "carbs": float(result.get("nf_total_carbohydrate", 0)),
            "fat": float(result.get("nf_total_fat", 0)),
        }

    # 2. Try FatSecret API
    fatsecret_data = get_fatsecret_data(query)
    if fatsecret_data:
        return {
            "match_name": fatsecret_data.get("name", original.title()),
            "calories": fatsecret_data.get("calories", 0),
            "protein": fatsecret_data.get("protein", 0),
            "carbs": fatsecret_data.get("carbs", 0),
            "fat": fatsecret_data.get("fat", 0),
        }

    # 3. Fuzzy match hardcoded fallback
    fallback_keys = list(hardcoded_nutrition.keys())
    fuzzy_match = get_close_matches(query, fallback_keys, n=1, cutoff=0.6)
    if fuzzy_match:
        fallback = hardcoded_nutrition[fuzzy_match[0]]
        return {
            "source":"Fallback",
            "match_name": fuzzy_match[0].title(),
            "calories": fallback["calories"],
            "protein": fallback["protein"],
            "carbs": fallback["carbs"],
            "fat": fallback["fat"],
        }

    # 4. Nothing found
    return {
        "error": f"No nutrition info found for '{original}'"
    }
