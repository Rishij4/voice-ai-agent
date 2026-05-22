
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
from app.services.tts_service import text_to_speech
from fastapi.staticfiles import StaticFiles
from app.models.database import engine
from app.models.appointment import Base
from app.agents.voice_agent import process_user_query
from app.services.stt_service import speech_to_text
from app.api.routes import router as api_router
from app.api.websocket import router as ws_router
from app.utils.latency_logger import LatencyLogger
app = FastAPI()
app.mount("/static", StaticFiles(directory="."), name="static")
Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
app.include_router(ws_router)
@app.get("/")
def home():
    return {"message": "Backend Running"}

@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
    logger = LatencyLogger()

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    logger.start("STT")

    text = speech_to_text(file_path)

    logger.stop("STT")
    language_map = {
        "en": "English",
        "hi": "Hindi",
        "ta": "Tamil"
    }

    detected_language = language_map.get(
        text["language"],
        "English"
    )

    logger.start("AI Processing")

    ai_response = process_user_query(
        text["text"],
        detected_language
    )

    logger.stop("AI Processing")

    logger.start("TTS")

    audio_file = text_to_speech(
        ai_response,
        text["language"]
    )

    logger.stop("TTS")
    logger.summary()

    return {
            "user_text": text["text"],
            "ai_response": ai_response,
            "language": text["language"],
            "audio_file": audio_file
        }
from fastapi.responses import FileResponse
from pydantic import BaseModel


class TTSRequest(BaseModel):
    text: str


@app.post("/text-to-speech")
async def generate_tts(request: TTSRequest):

    audio_path = text_to_speech(
        request.text,
        "en"
    )

    return FileResponse(
        audio_path,
        media_type="audio/mpeg",
        filename="response.mp3"
    )
