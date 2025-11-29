from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools import calculator

from app.core.settings import settings


SYSTEM_PROMPT = """
Você é um assistente em português.

- Para qualquer pergunta que envolva contas, operações matemáticas,
  porcentagens, raízes, potências, uso de fórmulas, etc.,
  você DEVE usar a ferramenta `calculator`.
- Para perguntas de conhecimento geral, responda normalmente.
- Sempre que usar a ferramenta, explique brevemente o resultado em linguagem natural.
"""


def build_agent() -> Agent:
    model = OllamaModel(
        host=settings.ollama_host,
        model_id=settings.ollama_model_id,
    )

    agent = Agent(
        model=model,
        tools=[calculator],
        system_prompt=SYSTEM_PROMPT,
    )
    return agent
