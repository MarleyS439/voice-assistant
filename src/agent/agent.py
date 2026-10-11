class Agent:
    def __init__(self, registry):
        self.registry = registry

    def execute_skill(self, skill_name: str, arguments: dict):
        skill = self.registry.get(skill_name)

        if skill is None:
            raise ValueError(f"Skill não encontrada: {skill_name}")

        return skill.execute(**arguments)
