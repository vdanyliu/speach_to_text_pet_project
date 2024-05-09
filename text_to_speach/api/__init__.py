from fastapi import APIRouter

from .platform import create_router as create_platform_router
from .text_to_speech import create_router as create_text_to_speach_router
from ..service.speech_to_text import ABCSpeachToTextService


def create_router(speach_to_text_service: ABCSpeachToTextService) -> APIRouter:
    router = APIRouter(prefix="/api/v1", tags=["api", "v1"])

    router.include_router(create_platform_router())
    router.include_router(create_text_to_speach_router(service=speach_to_text_service))

    return router
