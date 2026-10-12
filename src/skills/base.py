"""Classe base para todas as skills.

Uma skill expõe um conjunto de ferramentas (tools) que o LLM pode invocar.
Cada tool tem nome, descrição e schema de parâmetros (formato OpenAI).
A skill implementa execute() que despacha a ação para o método correto.
"""

from abc import ABC, abstractmethod


class Skill(ABC):
    """Contrato que toda skill deve seguir."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Nome curto e único da skill (ex: 'FileSystem')."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Descrição humana do que a skill faz."""
        ...

    @property
    @abstractmethod
    def tools(self) -> list[dict]:
        """Lista de tools no formato OpenAI function-calling.

        Cada tool: {"name": str, "description": str, "parameters": dict}
        """
        ...

    @abstractmethod
    def execute(self, tool_name: str, **kwargs) -> str:
        """Executa uma tool específica desta skill.

        Args:
            tool_name: Nome da tool (deve estar em self.tools).
            **kwargs: Parâmetros passados pelo LLM.
        Returns:
            Resultado em texto para o LLM/usuário.
        """
        ...
