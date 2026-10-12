"""Skill de aplicações — abrir, fechar e listar processos.

Usa ProcessHelper para interagir com processos do sistema.
"""

from subprocess import Popen

from helpers.process import ProcessHelper
from skills.base import Skill


class Application(Skill):

    @property
    def name(self) -> str:
        return "Application"

    @property
    def description(self) -> str:
        return "Abrir, fechar e listar aplicações/processos do sistema."

    @property
    def tools(self) -> list[dict]:
        return [
            {
                "name": "application_open",
                "description": "Abre uma aplicação.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "Comando para abrir a aplicação (ex: firefox, kate, dolphin).",
                        }
                    },
                    "required": ["command"],
                    "additionalProperties": False,
                },
            },
            {
                "name": "application_close",
                "description": "Fecha uma aplicação em execução pelo nome do processo.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Nome do processo (ex: firefox, kate).",
                        }
                    },
                    "required": ["name"],
                    "additionalProperties": False,
                },
            },
            {
                "name": "application_list",
                "description": "Lista os processos em execução do usuário atual.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False,
                },
            },
        ]

    def execute(self, tool_name: str, **kwargs) -> str:
        if tool_name == "application_open":
            return self._open(**kwargs)
        if tool_name == "application_close":
            return self._close(**kwargs)
        if tool_name == "application_list":
            return self._list(**kwargs)
        return f"Ação desconhecida: {tool_name}"

    def _open(self, command: str = "", **_) -> str:
        if not command:
            return "Comando não informado."
        ProcessHelper.start(command=command)
        return f"Abrindo {command}."

    def _close(self, name: str = "", **_) -> str:
        if not name:
            return "Nome não informado."
        if not ProcessHelper.is_running(name_process=name):
            return f"'{name}' não está em execução."
        pids = ProcessHelper.find_by_name(name=name)
        ProcessHelper.terminate(pids)
        return f"Fechei {len(pids)} processo(s) de '{name}'."

    def _list(self, **_) -> str:
        processes = ProcessHelper.list()
        return ProcessHelper.to_csv(processes=processes)
