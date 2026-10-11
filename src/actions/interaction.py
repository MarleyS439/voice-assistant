import json
import os
import subprocess
import tempfile
import wave

import requests
import sounddevice as sd
import numpy as np
from colorama import Fore, Style

from skills import registry
from src.memory.memory import HISTORY, MEMORY

from src.config import config


class Interaction:

    @staticmethod
    def record() -> str:

        print(f"\n{Fore.YELLOW}[Pressione ENTER para começar a falar]{Style.RESET_ALL}")
        input()
        print(f"{Fore.YELLOW}Gravando... pressione ENTER de novo para parar. {Style.RESET_ALL}")

        frames = []

        def callback(indata, frame_count, time_info, status):
            frames.append(indata.copy)

        stream = sd.InputStream(
            samplerate=config.SAMPLE_RATE,
            channels=1,
            dtype="int16",
            callback=callback
        )

        with stream:
            input()

        audio = np.concatenate(frames, axis=0)
        temp = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )

        with wave.open(f=temp.name, mode="wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(config.SAMPLE_RATE)
            wf.writeframes(audio.tobytes())
        return temp.name

    @staticmethod
    def transcribe(path_wav: str) -> str:
        segments, _ = config.WHISPER_MODEL.transcribe(
            path_wav,
            language=config.WHISPER_LANG
        )
        text = " ".join(seg.text.strip() for seg in segments)
        os.unlink(path_wav)
        return text.strip()

    @staticmethod
    def ask(text: str):
        HISTORY.append(
            {"role": "user", "content": text}
        )
        response = requests.post(
            config.OLLAMA_URL,
            json={
                "model": config.OLLAMA_MODEL,
                "messages": HISTORY,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        content = response.json()["message"]["content"]
        HISTORY.append(
            {"role": "assistant", "content": content}
        )

        return content

    @staticmethod
    def process(content: str) -> str:
        content = content.strip()

        if content.startswith("{"):
            try:
                data = json.loads(content)
                skill = data.get("action")
                params = data.get("params", {})
                if skill in registry.:
                    registry.
            except json.JSONDecodeError:
                pass
        return content

    @staticmethod
    def talk(text: str):
        print(f"{Fore.CYAN}Agente: {text}{Style.RESET_ALL}")

        temp_wav = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ).name

        try:
            subprocess.run(
                ["piper", "--model", config.PIPER_VOICE, "--output_file", temp_wav],
                input=text.encode("utf-8"),
                check=True
            )

            subprocess.run(["aplay", temp_wav], check=True)
        finally:
            if os.path.exists(temp_wav):
                os.unlink(temp_wav)
