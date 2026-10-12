"""Skill de navegador — abrir URLs e pesquisar na web.

Stub pronto para implementar.
"""

from skills.base import Skill


class Browser(Skill):

    @property
    def name(self) -> str:
        return "Browser"

    @property
    def description(self) -> str:
        return "Abre URLs e faz pesquisas na web no navegador padrão."

    @property
    def tools(self) -> list[dict]:
        return [
            {
                "name": "browser_open",
                "description": "Abre uma URL no navegador padrão.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL a abrir (ex: https://example.com).",
                        }
                    },
                    "required": ["url"],
                    "additionalProperties": False,
                },
            },
            {
                "name": "browser_search",
                "description": "Pesquisa um termo no navegador padrão.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Termo de busca.",
                        }
                    },
                    "required": ["query"],
                    "additionalProperties": False,
                },
            },
        ]

    def execute(self, tool_name: str, **kwargs) -> str:
        # TODO: usar webbrowser.open() do stdlib
        if tool_name == "browser_open":
            return f"Abrir URL '{kwargs.get('url', '')}': ainda não implementado."
        if tool_name == "browser_search":
            return f"Pesquisar '{kwargs.get('query', '')}': ainda não implementado."
        return f"Ação desconhecida: {tool_name}"
