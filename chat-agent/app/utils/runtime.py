from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from strands import Agent

from app.agent import build_agent
from app.core.logging import logger

_agent: Optional[Agent] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle da aplicação:
    - Inicializa o agente uma vez, na subida do servidor
    - Libera recursos no shutdown (se precisar no futuro)
    """
    global _agent
    logger.info("Inicializando agente Strands...")
    _agent = build_agent()
    logger.info("Agente Strands inicializado.")
    try:
        yield
    finally:
        logger.info("Encerrando aplicação FastAPI.")
        _agent = None


def get_agent() -> Agent:
    """
    Dependency para injetar o agente nas rotas FastAPI.
    """
    if _agent is None:
        raise RuntimeError("Agente não foi inicializado (lifespan não executado).")
    return _agent
