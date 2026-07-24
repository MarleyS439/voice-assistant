import os

from faster_whisper import WhisperModel

OLLAMA_URL = "http://localhost:41134/api/chat"
OLLAMA_MODEL = "qwen2.5:3b-instruct"
WHISPER_MODEL_SIZE = "small" # tiny/base/small/medium
WHISPER_LANG = "pt"

PIPER_VOICE = os.path.expanduser("~/.local/share/piper-voices/pt_BR-faber-medium.onnx")

SAMPLE_RATE = 16000

AGENDA_PATH = os.path.expanduser("~/.agenda.txt")

WHISPER_MODEL = WhisperModel(
    model_size_or_path=WHISPER_MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)

whisper_model = WhisperModel(
    WHISPER_MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)

SYSTEM_PROMPT = ""

AGENT_NAME = "Jarvis"