#!/usr/bin/env python3
"""Entry point do assistente de voz local.

Instancia todas as camadas, injeta dependências no VoiceAgent e
lança a janela Qt (PySide6).
"""

import sys
from pathlib import Path

# Garante que src/ está no PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import QApplication

from audio.stt import STT
from audio.tts import TTS
from llm.ollama import OllamaClient
from memory.conversation import Conversation
from skills.registry import SkillRegistry
from skills.application.skill import Application
from skills.filesystem.skill import FileSystem
from skills.weather.skill import Weather
from skills.browser.skill import Browser
from skills.terminal.skill import Terminal
from skills.memory.skill import Memory
from agent.voice_agent import VoiceAgent
from ui.main_window import MainWindow


def build_registry() -> SkillRegistry:
    """Registra todas as skills disponíveis."""
    registry = SkillRegistry()
    registry.register(Application())
    registry.register(FileSystem())
    registry.register(Weather())
    registry.register(Browser())
    registry.register(Terminal())
    registry.register(Memory())
    return registry


def main() -> None:
    # 1. Skills
    registry = build_registry()

    # 2. Memória (precisa das tools para o system prompt)
    conversation = Conversation(tools=registry.tools())

    # 3. Camadas de áudio e LLM
    stt = STT()
    tts = TTS()
    llm = OllamaClient()

    # 4. Agente
    agent = VoiceAgent(
        stt=stt,
        tts=tts,
        llm=llm,
        conversation=conversation,
        registry=registry,
    )

    # 5. UI Qt
    app = QApplication(sys.argv)
    window = MainWindow(agent)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
