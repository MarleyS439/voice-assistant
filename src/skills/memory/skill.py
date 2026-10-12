"""Skill de memória — anotações persistentes da conversa.

Stub pronto para implementar. Pode usar um arquivo JSON ou SQLite.
"""

from skills.base import Skill


class Memory(Skill):

    @property
    def name(self) -> str:
        return "Memory"

    @property
    def description(self) -> str:
        return "Armazena e recupera anotações/lembretes persistentes."

    @property
    def tools(self) -> list[dict]:
        return [
            {
                "name": "memory_save",
                "description": "Salva uma anotação.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "Texto da anotação a salvar.",
                        }
                    },
                    "required": ["content"],
                    "additionalProperties": False,
                },
            },
            {
                "name": "memory_recall",
                "description": "Recupera todas as anotações salvas.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False,
                },
            },
        ]

    def execute(self, tool_name: str, **kwargs) -> str:
        if tool_name == "memory_save":
            # TODO: salvar em arquivo
            return "Anotação salva com sucesso."
        if tool_name == "memory_recall":
            # TODO: ler do arquivo
            return "Nenhuma anotação encontrada."
        return f"Ação desconhecida: {tool_name}"
