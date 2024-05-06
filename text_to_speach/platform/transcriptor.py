import asyncio
import io
import pathlib
from dataclasses import dataclass
from functools import cached_property
from typing import IO, AsyncIterator

from google.cloud.speech_v2 import SpeechAsyncClient, StreamingRecognizeRequest, StreamingRecognitionFeatures
from google.cloud.speech_v2.types import cloud_speech
from google.oauth2.service_account import Credentials


@dataclass
class Config:
    chunk_size: int = 1024
    google_credentials: str = pathlib.Path("./google_credentials.json")


class GoogleSpeachToTextTranscriptor:
    def __init__(self, config: Config = Config()):
        self.config = config
        self.cloud_config = cloud_speech.RecognitionConfig({
            "auto_decoding_config": cloud_speech.AutoDetectDecodingConfig(),
            "language_codes": ["uk-UA"],
            "model": "long",
        })

    async def _asyncinit(self) -> "GoogleSpeachToTextTranscriptor":
        self.credentials: Credentials = Credentials.from_service_account_file(self.config.google_credentials)
        self.client = SpeechAsyncClient(credentials=self.credentials)
        return self

    async def transcribe(self, data: IO[bytes]) -> IO[str]:
        async for response in await self.client.streaming_recognize(self._chunked_audio_request(data)):
            for result in response.results:
                return io.StringIO(result.alternatives[0].transcript)

    async def transcribe_async_interim(self, data: IO[bytes]) -> AsyncIterator[str]:
        last_known_transcript = ""
        async for response in await self.client.streaming_recognize(self._chunked_stream_audio_request(data)):
            for result in response.results:
                if len(result.alternatives[0].transcript) > len(last_known_transcript):
                    last_known_transcript = result.alternatives[0].transcript
                    yield last_known_transcript
                if result.is_final:
                    yield result.alternatives[0].transcript

    @cached_property
    def _audio_config_interim(self) -> cloud_speech.StreamingRecognizeRequest:
        kwargs = dict(recognizer=f"projects/{self.credentials.project_id}/locations/global/recognizers/_",
                      streaming_config=cloud_speech.StreamingRecognitionConfig(
                          config=self.cloud_config,
                          streaming_features=StreamingRecognitionFeatures(interim_results=True)), )
        return cloud_speech.StreamingRecognizeRequest(**kwargs)

    @cached_property
    def _audio_config(self) -> cloud_speech.StreamingRecognizeRequest:
        kwargs = dict(
            recognizer=f"projects/{'caramel-core-203714'}/locations/global/recognizers/_",
            streaming_config=cloud_speech.StreamingRecognitionConfig(
                config=self.cloud_config,
            ),
        )
        return cloud_speech.StreamingRecognizeRequest(**kwargs)

    async def _chunked_audio_request(self, data: IO[bytes]) -> AsyncIterator[StreamingRecognizeRequest]:
        yield self._audio_config
        while chunk := data.read(self.config.chunk_size):
            yield cloud_speech.StreamingRecognizeRequest(audio=chunk)

    async def _chunked_stream_audio_request(self, data: IO[bytes]) -> AsyncIterator[StreamingRecognizeRequest]:
        yield self._audio_config_interim
        while chunk := data.read(self.config.chunk_size):
            yield cloud_speech.StreamingRecognizeRequest(audio=chunk)
