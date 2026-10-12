"""Speech-to-Text usando faster-whisper.

Suporta dois modos:
- record(): bloquante com input() (CLI)
- start_recording() / stop_recording(): não-bloqueante (UI)
"""

import os
import tempfile
import wave

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from colorama import Fore, Style

from config.settings import WHISPER_MODEL_SIZE, WHISPER_LANG, SAMPLE_RATE


class STT:
    """Fachada para captura de áudio e transcrição via Whisper."""

    def __init__(self):
        print(f"{Fore.YELLOW}Carregando modelo Whisper (STT)...{Style.RESET_ALL}")
        self._model = WhisperModel(
            model_size_or_path=WHISPER_MODEL_SIZE,
            device="cpu",
            compute_type="int8",
        )
        self._frames: list[np.ndarray] = []
        self._stream: sd.InputStream | None = None

    # ── Modo CLI (bloqueante) ───────────────────────────────────────────────

    def record(self) -> str:
        """Grava áudio via microfone (ENTER para iniciar/parar) → caminho .wav."""
        print(f"\n{Fore.YELLOW}[ENTER para falar · ENTER para parar]{Style.RESET_ALL}")
        input()
        print(f"{Fore.YELLOW}Gravando...{Style.RESET_ALL}")

        frames: list[np.ndarray] = []

        def callback(indata, frame_count, time_info, status):
            frames.append(indata.copy())

        with sd.InputStream(
            samplerate=SAMPLE_RATE, channels=1, dtype="int16", callback=callback
        ):
            input()

        audio = np.concatenate(frames, axis=0)
        return self._save_wav(audio)

    # ── Modo UI (não-bloqueante) ─────────────────────────────────────────────

    def start_recording(self) -> None:
        """Inicia captura de áudio do microfone (não-bloqueante)."""
        self._frames = []

        def callback(indata, frame_count, time_info, status):
            self._frames.append(indata.copy())

        self._stream = sd.InputStream(
            samplerate=SAMPLE_RATE, channels=1, dtype="int16", callback=callback
        )
        self._stream.start()

    def stop_recording(self) -> str:
        """Para a captura e retorna o caminho do arquivo .wav gravado."""
        if self._stream is None:
            return ""

        self._stream.stop()
        self._stream.close()
        self._stream = None

        if not self._frames:
            return ""

        audio = np.concatenate(self._frames, axis=0)
        return self._save_wav(audio)

    # ── Transcrição ──────────────────────────────────────────────────────────

    def transcribe(self, wav_path: str) -> str:
        """Transcreve um arquivo .wav → texto. Remove o arquivo ao final."""
        segments, _ = self._model.transcribe(wav_path, language=WHISPER_LANG)
        text = " ".join(seg.text.strip() for seg in segments)
        os.unlink(wav_path)
        return text.strip()

    # ── Util ──────────────────────────────────────────────────────────────────

    @staticmethod
    def _save_wav(audio: np.ndarray) -> str:
        """Salva array numpy como arquivo .wav temporário e retorna o caminho."""
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio.tobytes())
        return tmp.name
