"""Teste de sanidade: registra skills e verifica tools disponíveis."""

from skills.registry import SkillRegistry
from skills.application.skill import Application
from skills.filesystem.skill import FileSystem
from skills.weather.skill import Weather
from skills.browser.skill import Browser
from skills.terminal.skill import Terminal
from skills.memory.skill import Memory


def main():
    registry = SkillRegistry()
    registry.register(Application())
    registry.register(FileSystem())
    registry.register(Weather())
    registry.register(Browser())
    registry.register(Terminal())
    registry.register(Memory())

    tools = registry.tools()
    print(f"Skills registradas: {len(registry.all())}")
    print(f"Tools disponíveis: {len(tools)}")
    for t in tools:
        print(f"  - {t['name']}: {t['description'][:60]}")


if __name__ == "__main__":
    main()
