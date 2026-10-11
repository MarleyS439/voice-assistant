from skills.base import Skill


class Weather(Skill):

    @property
    def name(self) -> str:
        return "Consulta clima"

    @property
    def description(self) -> str:
        return "Skill de consulta de clima"

    @property
    def execute(self, **kwargs):
        ...