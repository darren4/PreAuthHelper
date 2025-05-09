import json


def get_secret(key: str) -> str:
    with open("secrets.json", "r") as f:
        secrets = json.load(f)
        return secrets[key]


def save_audio(path: str, audio: bytes):
    with open(path, "wb") as f:
        f.write(audio)
