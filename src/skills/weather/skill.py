"""Skill de consulta de clima — stub pronto para implementar.

Usar GeocodingHelper para coordenadas + Open-Meteo (ou similar) para previsão.
"""

from skills.base import Skill


class Weather(Skill):

    @property
    def name(self) -> str:
        return "Weather"

    @property
    def description(self) -> str:
        return "Consulta o clima atual de uma cidade."

    @property
    def tools(self) -> list[dict]:
        return [
            {
                "name": "weather_query",
                "description": "Consulta o clima atual de uma cidade.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "Nome da cidade (ex: São Paulo, Rio de Janeiro).",
                        }
                    },
                    "required": ["city"],
                    "additionalProperties": False,
                },
            },
        ]

    def execute(self, tool_name: str, **kwargs) -> str:
        if tool_name == "weather_query":
            city = kwargs.get("city", "")
            # TODO: usar GeocodingHelper.coordinates() + Open-Meteo API
            return f"Clima de '{city}': funcionalidade ainda não implementada."
        return f"Ação desconhecida: {tool_name}"
