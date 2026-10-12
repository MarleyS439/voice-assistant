"""Interface de linha de comando (CLI).

Delega toda a lógica para VoiceAgent.run().
"""

from agent.voice_agent import VoiceAgent


class CLI:

    def __init__(self, agent: VoiceAgent):
        self._agent = agent

    def run(self) -> None:
        self._agent.run()
