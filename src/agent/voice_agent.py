"""Agente de voz — orquestrador principal.

Conecta as camadas: STT → Conversation + LLM → processar resposta → TTS.
Se o LLM responde com JSON de ação, despacha para o SkillRegistry.

Dois modos:
- run(): loop CLI (input/ENTER para gravar)
- process_turn(user_text): ciclo único (UI chama com texto já transcrito)
"""

import json

from audio.stt import STT
from audio.tts import TTS
from llm.ollama import OllamaClient
from memory.conversation import Conversation
from skills.registry import SkillRegistry
from colorama import Fore, Style


class VoiceAgent:
    """Orquestra o ciclo: ouvir → pensar → falar."""

    def __init__(
        self,
        stt: STT,
        tts: TTS,
        llm: OllamaClient,
        conversation: Conversation,
        registry: SkillRegistry,
    ):
        self._stt = stt
        self._tts = tts
        self._llm = llm
        self._conversation = conversation
        self._registry = registry

    # ── Modo CLI ─────────────────────────────────────────────────────────────

    def run(self) -> None:
        """Loop principal do agente (CLI). Ctrl+C para sair."""
        print(
            f"{Fore.LIGHTGREEN_EX}Agente de voz local pronto. "
            f"Ctrl+C para sair.\n{Style.RESET_ALL}"
        )

        try:
            while True:
                # 1. Ouvir
                wav_path = self._stt.record()
                user_text = self._stt.transcribe(wav_path)

                if not user_text:
                    print(f"{Fore.YELLOW}(Nada entendido, tente de novo){Style.RESET_ALL}")
                    continue

                print(f"{Fore.LIGHTGREEN_EX}Você: {user_text}{Style.RESET_ALL}")

                # Comando de saída
                if user_text.lower().strip() in ("sair", "encerrar", "tchau"):
                    self._tts.speak("Até mais!")
                    break

                # 2. Processar
                final = self.process_turn(user_text)

                # 3. Falar
                self._tts.speak(final)

        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}\nEncerrando...{Style.RESET_ALL}")

    # ── Modo UI ──────────────────────────────────────────────────────────────

    def process_turn(self, user_text: str) -> str:
        """Processa um turno completo: LLM → dispatch → retorna resposta.

        Não toca áudio (a UI decide como apresentar/falar a resposta).

        Args:
            user_text: Texto já transcrito do usuário.
        Returns:
            Resposta final do agente (texto ou resultado de ação).
        """
        # Comando de saída
        if user_text.lower().strip() in ("sair", "encerrar", "tchau"):
            return "Até mais!"

        # 1. Pensar
        self._conversation.add_user(user_text)
        raw_response = self._llm.chat(self._conversation.messages)
        self._conversation.add_assistant(raw_response)

        # 2. Processar (ação ou texto puro)
        return self._process(raw_response)

    def speak(self, text: str) -> None:
        """Sintetiza e reproduz texto em voz alta (delega para TTS)."""
        self._tts.speak(text)

    # ── Lógica interna ────────────────────────────────────────────────────────

    def _process(self, content: str) -> str:
        """Se o conteúdo for JSON de ação, despacha para o registry.

        Caso contrário, retorna o texto puro.
        """
        content = content.strip()
        if content.startswith("{"):
            try:
                data = json.loads(content)
                tool = data.get("action") or data.get("tool")
                params = data.get("params", {})

                if tool:
                    result = self._registry.dispatch(tool, params)
                    # O resultado de uma ação volta para o LLM como contexto,
                    # mas por simplicidade retornamos direto para o usuário.
                    return result
            except json.JSONDecodeError:
                pass
        return content
