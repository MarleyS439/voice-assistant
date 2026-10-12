"""Memória de conversa — mantém o histórico de mensagens.

Gerencia a lista de mensagens no formato Ollama/OpenAI:
[{"role": "system|user|assistant", "content": "..."}]
"""

from config.persona import build_system_prompt


class Conversation:
    """Histórico de mensagens com prompt de sistema dinâmico."""

    def __init__(self, tools: list[dict] | None = None):
        system_prompt = build_system_prompt(tools or [])
        self._messages: list[dict] = [
            {"role": "system", "content": system_prompt}
        ]

    @property
    def messages(self) -> list[dict]:
        """Lista imutável das mensagens atuais."""
        return list(self._messages)

    def add_user(self, content: str) -> None:
        self._messages.append({"role": "user", "content": content})

    def add_assistant(self, content: str) -> None:
        self._messages.append({"role": "assistant", "content": content})

    def reset(self, tools: list[dict] | None = None) -> None:
        """Recria o histórico com prompt de sistema atualizado."""
        system_prompt = build_system_prompt(tools or [])
        self._messages = [{"role": "system", "content": system_prompt}]
