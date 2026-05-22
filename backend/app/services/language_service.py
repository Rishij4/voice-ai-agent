def detect_language(text):
    if "नमस्ते" in text:
        return "Hindi"

    if "வணக்கம்" in text:
        return "Tamil"

    return "English"