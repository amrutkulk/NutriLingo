import os
import openai
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def translate_text(text, target_language="en") -> list[str]:
    """Translate each line of text and return a list of translated items."""
    prompt = f"Translate the following restaurant menu into {target_language}. Keep each item on its own line:\n\n{text}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful restaurant menu translator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        translated_block = response['choices'][0]['message']['content'].strip()
        return [line.strip() for line in translated_block.split("\n") if line.strip()]
    except Exception as e:
        try:
            # Fallback to Google Translate entire block
            fallback_text = GoogleTranslator(source='auto', target=target_language).translate(text)
            return [line.strip() for line in fallback_text.split("\n") if line.strip()]
        except Exception as fallback_error:
            return [f"[Translation failed: {str(fallback_error)}]"]

