"""Registro central de skills.

O registry mantém as skills instanciadas e fornece:
- register(skill): adiciona uma skill
- get_tool(name): busca uma tool pelo nome, retorna (skill, tool_name)
- tools(): lista todas as tools (para injetar no prompt do LLM)
- dispatch(tool_name, params): encontra a skill e executa a tool
"""

from skills.base import Skill


class SkillRegistry:

    def __init__(self):
        self._skills: dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        self._skills[skill.name] = skill

    def get(self, skill_name: str) -> Skill | None:
        return self._skills.get(skill_name)

    def all(self) -> list[Skill]:
        return list(self._skills.values())

    def descriptions(self) -> list[dict[str, str]]:
        return [
            {"name": s.name, "description": s.description}
            for s in self._skills.values()
        ]

    def tools(self) -> list[dict]:
        """Lista todas as tools de todas as skills."""
        return [
            tool
            for skill in self._skills.values()
            for tool in skill.tools
        ]

    def tool_map(self) -> dict[str, tuple[Skill, str]]:
        """Mapeia nome_da_tool → (skill, tool_name) para dispatch."""
        result = {}
        for skill in self._skills.values():
            for tool in skill.tools:
                result[tool["name"]] = (skill, tool["name"])
        return result

    def dispatch(self, tool_name: str, params: dict) -> str:
        """Encontra a skill responsável e executa a tool.

        Returns:
            Resultado em texto, ou mensagem de erro se a tool não existe.
        """
        mapping = self.tool_map()
        if tool_name not in mapping:
            return f"Ferramenta '{tool_name}' não encontrada."
        skill, name = mapping[tool_name]
        return skill.execute(tool_name=name, **params)
