from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuração central da aplicação.

    Os nomes das variáveis de ambiente começam com CHAT_*
    ex.: CHAT_OLLAMA_HOST, CHAT_OLLAMA_MODEL_ID
    """

    ollama_host: str = "http://localhost:11434"
    ollama_model_id: str = "llama3"

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="CHAT_",
        extra="ignore",
    )


settings = Settings()
