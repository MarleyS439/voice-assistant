"""Skill de terminal — executar comandos shell.

Stub pronto para implementar. Por segurança, deve usar whitelist de comandos.
"""

from skills.base import Skill


class Terminal(Skill):

    @property
    def name(self) -> str:
        return "Terminal"

    @property
    def description(self) -> str:
        return "Executa comandos no terminal (com whitelist de segurança)."

    @property
    def tools(self) -> list[dict]:
        return [
            {
                "name": "terminal_run",
                "description": "Executa um comando no terminal.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "Comando a executar.",
                        }
                    },
                    "required": ["command"],
                    "additionalProperties": False,
                },
            },
        ]

    def execute(self, tool_name: str, **kwargs) -> str:
        if tool_name == "terminal_run":
            # TODO: implementar whitelist de comandos seguros
            return "Terminal: funcionalidade ainda não implementada."
        return f"Ação desconhecida: {tool_name}"
