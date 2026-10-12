"""Cliente LLM usando Ollama.

Comunicação simples via API REST do Ollama (/api/chat).
"""

import requests

from config.settings import OLLAMA_URL, OLLAMA_MODEL


class OllamaClient:
    """Fachada para o Ollama."""

    def __init__(self):
        self._url = OLLAMA_URL
        self._model = OLLAMA_MODEL

    def chat(self, messages: list[dict]) -> str:
        """Envia mensagens e retorna o conteúdo da resposta.

        Args:
            messages: Lista de dicts no formato
                      [{"role": "system|user|assistant", "content": "..."}]
        Returns:
            Conteúdo textual da resposta do modelo.
        """
        response = requests.post(
            self._url,
            json={
                "model": self._model,
                "messages": messages,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["message"]["content"]
