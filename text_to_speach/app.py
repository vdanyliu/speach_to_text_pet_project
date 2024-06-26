from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from text_to_speach.api import create_router
from text_to_speach.platform.transcriptor import GoogleSpeechToTextTranscriptor
from text_to_speach.service.speech_to_text import SpeechToTextService, ABCSpeechToTextService


def create_transcribe_service(app: FastAPI) -> ABCSpeechToTextService:
    transcriptor = GoogleSpeechToTextTranscriptor()
    transcribe_service = SpeechToTextService(transcriptor=transcriptor)
    app.add_event_handler("startup", transcribe_service._async_init)
    return transcribe_service


def create_app() -> FastAPI:
    app = FastAPI()
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    transcribe_service = create_transcribe_service(app)
    api_router = create_router(speach_to_text_service=transcribe_service)
    app.include_router(api_router)

    return app
