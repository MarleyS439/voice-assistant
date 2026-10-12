"""Persona do agente — constrói o system prompt dinamicamente.

O system prompt é montado a partir da lista de tools registradas,
para que o LLM sempre saiba o que pode chamar.
"""

import json

from config.settings import AGENT_NAME, USER_NAME


def build_system_prompt(tools: list[dict]) -> str:
    """Monta o prompt de sistema com as tools disponíveis.

    Args:
        tools: Lista de dicts no formato OpenAI function-calling,
               ex: [{"name": "...", "description": "...", "parameters": {...}}]
    """
    tools_json = json.dumps(tools, ensure_ascii=False, indent=2)

    return f"""Você é {AGENT_NAME}, um assistente de voz local rodando no computador de {USER_NAME}.
Responda sempre em português do Brasil, de forma curta e natural (texto puro, sem markdown).

Você pode fazer duas coisas:
1. Responder normalmente em texto.
2. Pedir para executar UMA ação, respondendo SOMENTE com um JSON no formato:
   {{"action": "nome_da_action", "params": {{...}}}}

Ferramentas disponíveis nesta interação:
{tools_json}

Se o pedido do usuário não corresponder a nenhuma ferramenta, apenas responda em texto.
Nunca invente ações fora da lista. Nunca use markdown.
"""
