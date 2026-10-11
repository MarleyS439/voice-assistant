from typing import Any

import requests


class GeocodingHelper:
    @staticmethod
    def get_address(query: str) -> dict[str, str]:
        try:
            url = "https://nominatim.openstreetmap.org/search"
            headers = {
                "User-Agent": "Application/1.0 (application@email.com)"
            }
            params = {
                "q": query.strip(),
                "format": "json",
                "addressdetails": 1,
                "limit": 1
            }
            response = requests.get(url=url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            result = data[0].get("address", {})

            return {
                "logradouro": result["road"],
                "bairro": result["suburb"],
                "cidade": result["city"],
                "estado": result["state"],
                "regiao": result["region"],
                "cep": result["postcode"],
                "pais": result["country"]
            }
        except Exception as e:
            raise f"Ocorreu um erro: {e}"

    @staticmethod
    def coordinates(address: dict[str, str]) -> dict[str, Any] | None:

        try:
            cep = address["cep"].replace("-", "").strip()
            url = f"https://brasilapi.com.br/api/cep/v2/{cep}"
            response = requests.get(url=url, timeout=10)
            response.raise_for_status()
            data = response.json()
            coord = data.get("location", {}).get("coordinates", {})

            return {
                "cep": data.get("cep"),
                "cidade": data.get("city"),
                "estado": data.get("state"),
                "latitude": coord.get("latitude"),
                "longitude": coord.get("longitude"),
            }
        except Exception as error:
            print(f"Erro: {error}")
