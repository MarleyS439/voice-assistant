from skills.application import skill
from skills.base import Skill


class SkillRegistry:

    def __init__(self):
        self._skills: dict[str, Skill] = {}

    def register(self, skill):
        self._skills[skill.name] = skill

    def get(self, name: str) -> Skill | None:
        return self._skills.get(name)

    def all(self) -> list[Skill]:
        return list(self._skills.values())

    def descriptions(self) -> list[dict[str, str]]:
        return [
            {
                "name": skill.name,
                "description": skill.description
            }

            for skill in self._skills.values()
        ]
