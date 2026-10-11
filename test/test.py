from skills.registry import SkillRegistry
from skills.application.skill import Applications
from skills.filesystem.skill import FileSystem

registry = SkillRegistry()

registry.register(Applications())
registry.register(FileSystem())

available_skills = registry.descriptions()

print(available_skills)