from utils import get_secret

from elevenlabs import stream
from elevenlabs.client import ElevenLabs
import requests
import typing
from io import BytesIO


def get_voice(text: str) -> bytes:
    url = "https://api.elevenlabs.io/v1/text-to-speech/JBFqnCBsd6RMkjVDRZzb"
    headers = {
        "xi-api-key": get_secret("ELEVENLABS_SECRET_KEY"),
        "Content-Type": "application/json"
    }
    body = {
        "text": text
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.content


def get_text(audio: bytes) -> str:
    """
    SpeechToTextChunkResponseModel(language_code='eng', language_probability=1.0, text='Hello.', words=[SpeechToTextWordResponseModel(text='Hello.', start=0.079, end=0.459, type='word', speaker_id='speaker_0', characters=None)], additional_formats=None)
    """
    client = ElevenLabs(
        api_key=get_secret("ELEVENLABS_SECRET_KEY"),
    )
    audio_data = BytesIO(audio)
    transcription = client.speech_to_text.convert(
    file=audio_data,
    model_id="scribe_v1", # Model to use, for now only "scribe_v1" is supported
    language_code="eng", # Language of the audio file. If set to None, the model will detect the language automatically.
    diarize=True, # Whether to annotate who is speaking
    )
    return transcription
