"""Skill de filesystem — operações com arquivos e diretórios.

Usa FileSystemHelper para listar, verificar existência, ler, criar, etc.
"""

from helpers.filesystem import FileSystemHelper
from skills.base import Skill


class FileSystem(Skill):

    @property
    def name(self) -> str:
        return "FileSystem"

    @property
    def description(self) -> str:
        return (
            "Gerencia arquivos e diretórios: lista, verifica existência, "
            "lê, cria, copia, move, renomeia e exclui itens."
        )

    @property
    def tools(self) -> list[dict]:
        return [
            {
                "name": "filesystem_list_directory",
                "description": "Lista os arquivos e diretórios de um caminho.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Caminho do diretório a listar.",
                        }
                    },
                    "required": ["path"],
                    "additionalProperties": False,
                },
            },
            {
                "name": "filesystem_exists",
                "description": "Verifica se um arquivo ou diretório existe.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Caminho a verificar.",
                        }
                    },
                    "required": ["path"],
                    "additionalProperties": False,
                },
            },
        ]

    def execute(self, tool_name: str, **kwargs) -> str:
        if tool_name == "filesystem_list_directory":
            return self._list_directory(**kwargs)
        if tool_name == "filesystem_exists":
            return self._exists(**kwargs)
        return f"Ação desconhecida: {tool_name}"

    def _list_directory(self, path: str = "", **_) -> str:
        if not path:
            return "Caminho não informado."
        try:
            items = FileSystemHelper.list_directory(path)
            lines = [
                f"{'[DIR] ' if i['is_directory'] else '[FILE] '}{i['name']}"
                for i in items
            ]
            return "\n".join(lines) if lines else "Diretório vazio."
        except NotADirectoryError:
            return f"'{path}' não é um diretório válido."

    def _exists(self, path: str = "", **_) -> str:
        if not path:
            return "Caminho não informado."
        exists = FileSystemHelper.exists(path)
        return f"'{path}' existe." if exists else f"'{path}' não existe."
