from abc import ABC, abstractmethod
from pathlib import Path
from typing import IO, AsyncIterator

from text_to_speach.platform.transcriptor import GoogleSpeechToTextTranscriptor


class ABCSpeachToTextService(ABC):
    @abstractmethod
    async def transcribe(self, data: IO[bytes]) -> IO[str]:
        pass

    @abstractmethod
    async def transcribe_interim(self, data: IO[bytes]) -> AsyncIterator[str]:
        pass


class SpeachToTextService(ABCSpeachToTextService):
    def __init__(self, transcriptor: GoogleSpeechToTextTranscriptor):
        self._transcriptor = transcriptor

    async def _async_init(self):
        await self._transcriptor._asyncinit()

    async def transcribe(self, data: IO[bytes]) -> IO[str]:
        return await self._transcriptor.transcribe(data)

    async def transcribe_interim(self, data: IO[bytes]) -> AsyncIterator[str]:
        async for result in self._transcriptor.transcribe_async_interim(data):
            yield result
