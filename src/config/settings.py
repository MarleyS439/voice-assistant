"""Configurações centralizadas do assistente de voz.

Carrega variáveis do arquivo .env via python-dotenv.
Nenhum import pesado (ex: WhisperModel) acontece aqui — quem precisa
do modelo importa settings e instancia sob demanda.
"""

import os

from dotenv import load_dotenv

load_dotenv()


# ── Ollama ────────────────────────────────────────────────────────────────
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b-instruct")

# ── Whisper (STT) ──────────────────────────────────────────────────────────
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base")
WHISPER_LANG = os.getenv("WHISPER_LANG", "pt")

# ── Piper (TTS) ────────────────────────────────────────────────────────────
PIPER_VOICE = os.path.expanduser(
    os.getenv("PIPER_VOICE", "~/.local/share/piper-voices/pt_BR-faber-medium.onnx")
)

# ── Áudio ──────────────────────────────────────────────────────────────────
SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", "16000"))

# ── Agente / Usuário ────────────────────────────────────────────────────────
AGENT_NAME = os.getenv("AGENT_NAME", "Assistente")
USER_NAME = os.getenv("USER_NAME", "Usuário")

# ── Caminhos autorizados para skills de filesystem ──────────────────────────
AUTHORIZED_PATHS = {
    os.path.expanduser(f"~/{USER_NAME}/Programas/agent/"),
    os.path.expanduser("~/Downloads/"),
}

# ── Agenda ──────────────────────────────────────────────────────────────────
AGENDA_PATH = os.path.expanduser("~/.agenda.txt")
