from faster_whisper import WhisperModel

model = WhisperModel("tiny")

def speech_to_text(audio_file):

    segments, info = model.transcribe(
    audio_file,
    beam_size=5
)

    full_text = ""

    for segment in segments:
        full_text += segment.text

    return {
        "text": full_text,
        "language": info.language
    }