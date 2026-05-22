from app.services.stt_service import speech_to_text
from app.agents.voice_agent import process_user_query
from app.services.tts_service import text_to_speech

# Step 1 — Speech to Text
stt_result = speech_to_text("sample.wav")

user_text = stt_result["text"]

language = stt_result["language"]

print("User Said:", user_text)
print("Detected Language:", language)

# Map Whisper codes
if language == "en":
    language_name = "English"

elif language == "hi":
    language_name = "Hindi"

elif language == "ta":
    language_name = "Tamil"

else:
    language_name = "English"

# Step 2 — AI Processing
ai_response = process_user_query(
    user_text,
    language_name
)

print("AI Response:", ai_response)

# Step 3 — Text to Speech

language_code = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta"
}

audio_file = text_to_speech(
    ai_response,
    language_code[language_name]
)

print("Generated Audio:", audio_file)