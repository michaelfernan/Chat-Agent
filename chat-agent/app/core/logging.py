import logging


def setup_logging() -> logging.Logger:
    """
    Configuração simples de logging para a API.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    logger = logging.getLogger("chat-agent")
    logger.info("Logging inicializado")
    return logger


logger = setup_logging()
