import os
from faster_whisper import WhisperModel


class Config:
    def __init__(self, config):
        self.config = config


# Ollama
OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

# Whisper
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base")
WHISPER_LANG = os.getenv("WHISPER_LANG")
WHISPER_MODEL = WhisperModel(
    model_size_or_path=WHISPER_MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)

# Piper
PIPER_VOICE = os.path.expanduser(os.getenv("PIPER_VOICE", ""))
SAMPLE_RATE = os.getenv("SAMPLE_RATE", 16000)

# Agent
AGENT_NAME = os.getenv("AGENT_NAME")

# Calendar
AGENDA_PATH = os.path.expanduser("~/.agenda.txt")

# User
USER_NAME = os.getenv("USER_NAME")

# Authorized Paths
AUTHORIZED_PATHS = {
    f"~/{USER_NAME}/Programas/agent/",
    f"~/{USER_NAME}/Downloads/"
}

# System Prompt
SYSTEM_PROMPT = """

"""