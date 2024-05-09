import io
from typing import AsyncIterator, IO

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

from text_to_speach.service.speech_to_text import ABCSpeachToTextService


def create_router(service: ABCSpeachToTextService) -> APIRouter:
    router = APIRouter(prefix='/transcribe', tags=['transcribe'])

    @router.post('/file')
    async def transcribe_file(file: UploadFile = File(...)):
        try:
            return StreamingResponse(await service.transcribe(file.file), media_type="text/plain")
        except Exception as e:
            raise HTTPException(status_code=500, detail={"error_type": type(e).__name__, "message": str(e)})

    @router.post('/file/sse')
    async def transcribe_file(file: UploadFile = File(...)):
        async def generate_massage(file: IO) -> AsyncIterator[str]:
            async for data in service.transcribe_interim(file):
                yield f"data: {data}\n\n"

        try:
            return StreamingResponse(
                generate_massage(file=io.BytesIO(file.file.read())),media_type="text/event-stream")
        except Exception as e:
            raise HTTPException(status_code=500, detail={"error_type": type(e).__name__, "message": str(e)})

    return router
