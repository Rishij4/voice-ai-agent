from gtts import gTTS
import os

def text_to_speech(text, language="en"):

    output_path = "response.mp3"

    # delete old file if exists
    if os.path.exists(output_path):
        os.remove(output_path)

    # Safe language mapping
    language_map = {
        "english": "en",
        "en": "en",

        "hindi": "hi",
        "hi": "hi",

        "tamil": "ta",
        "ta": "ta"
    }

    # fallback to english
    safe_language = language_map.get(
        str(language).lower(),
        "en"
    )

    tts = gTTS(
        text=text,
        lang=safe_language,
        slow=False
    )

    tts.save(output_path)

    return output_path