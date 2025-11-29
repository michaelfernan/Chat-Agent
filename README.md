# 🚀 Chat Agent — FastAPI + Strands Agents + Ollama

Case técnico: **API de Chat com Agente de IA**, capaz de:

- 💬 conversar sobre conhecimento geral  
- ➗ usar uma **tool de cálculo matemático** para resolver operações automaticamente

Stack utilizada:

- **FastAPI** → API HTTP  
- **Strands Agents** → orquestração do agente  
- **Ollama** → LLM local  
- **strands-agents-tools** → tool `calculator`  
- **Pytest** → testes automatizados  
- **Docker / Docker Compose** → empacotamento da API

---

## 🧠 Visão Geral da Arquitetura

1. O cliente envia `POST /chat` com `{ "message": "..." }`.
2. O FastAPI repassa a mensagem para o **Agent** carregado no startup (lifespan).
3. O Agent:
   - usa `OllamaModel` apontando para o host configurado (ex.: `http://host.docker.internal:11434` via Docker, ou `http://127.0.0.1:11434` local);
   - possui a tool `calculator` configurada.
4. O LLM decide:
   - responder diretamente, ou  
   - acionar a tool para cálculos.
5. A API retorna um JSON no formato `{ "response": "..." }`.

---

## 🗂 Estrutura de Pastas

```bash
app/
├── api/
│   ├── __init__.py
│   └── routes_chat.py          # endpoint POST /chat
├── agent/
│   ├── __init__.py
│   ├── builder.py              # construção do Agent
│   └── tools.py                # espaço para tools extras
├── core/
│   ├── __init__.py
│   ├── logging.py              # logging customizado
│   └── settings.py             # Pydantic Settings (.env)
├── schemas/
│   ├── __init__.py
│   └── chat.py                 # ChatRequest / ChatResponse
├── utils/
│   ├── __init__.py
│   └── runtime.py              # lifespan + get_agent
└── main.py                     # App FastAPI + /health
```

---

## ⚙️ Configuração do Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto:

```env
# Host/modelo usados pela aplicação (modo local)
CHAT_OLLAMA_HOST=http://127.0.0.1:11434
CHAT_OLLAMA_MODEL_ID=llama3.1

# Configuração de host/porta da API
CHAT_API_HOST=0.0.0.0
CHAT_API_PORT=8000
```

> No ambiente Docker, essas variáveis podem ser sobrescritas no `docker-compose.yml`.

---

## 🐍 Rodando Localmente (sem Docker)

### 1️⃣ Criar e ativar ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2️⃣ Instalar dependências

```bash
pip install .
```

ou, alternativamente:

```bash
pip install fastapi uvicorn[standard] pydantic pydantic-settings strands-agents strands-agents-tools ollama pytest
```

---

## 🤖 Configurar e rodar o Ollama (host)

### Instalação

Siga a documentação oficial do Ollama para Linux. Exemplo (padrão script oficial):

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

> **Obs.:** em ambiente Docker é importante que o servidor Ollama esteja rodando **no host** escutando em `127.0.0.1:11434`, pois o container vai acessá‑lo via `host.docker.internal`.

### Baixar o modelo

> ⚠️ Importante:  
> `llama3` **não suporta tools**.  
> Use **`llama3.1`**.

```bash
ollama pull llama3.1
```

### Subir o servidor Ollama

```bash
ollama serve
```

(Ou habilite o serviço para subir automaticamente, conforme a instalação.)

---

## 🏃‍♂️ Rodando o Servidor FastAPI (local)

Com o ambiente virtual ativo e o Ollama rodando:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Endpoints principais:

- Health Check → `GET /health`
- Chat → `POST /chat`

---

## 🐳 Rodando com Docker / Docker Compose

O projeto inclui suporte a Docker. Exemplo de `docker-compose.yml`:

```yaml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: chat-agent-api
    restart: unless-stopped
    environment:
      # Ollama rodando no HOST, acessível via host.docker.internal
      OLLAMA_HOST: "http://host.docker.internal:11434"
      CHAT_OLLAMA_HOST: "http://host.docker.internal:11434"
      CHAT_OLLAMA_MODEL_ID: "llama3.1"

      CHAT_API_HOST: "0.0.0.0"
      CHAT_API_PORT: "8000"
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

> Certifique‑se de que o **Ollama está rodando no host** antes de subir o container.

### Subir a API via Docker

```bash
docker compose up --build
```

Verificar:

```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

---

## 🔍 Endpoints

### `GET /health`

```json
{ "status": "ok" }
```

---

### `POST /chat`

#### Exemplo de requisição:

```json
{
  "message": "Qual a raiz quadrada de 144?"
}
```

#### Exemplo de resposta:

```json
{
  "response": "A raiz quadrada de 144 é 12.
"
}
```

Nos logs do servidor é possível ver o uso da tool:

```text
Tool #2: calculator
```

---

## 🧪 Testes Automatizados

Os testes utilizam **pytest** e o `TestClient` do FastAPI.

Arquivo principal de teste:

```text
app/tests/test_chat_endpoint.py
```

### Pré‑requisitos para os testes passarem

1. Dependências instaladas no ambiente virtual:
   ```bash
   pip install .
   pip install pytest
   ```
2. Servidor do **Ollama rodando** e acessível no host configurado em `CHAT_OLLAMA_HOST`
   (por padrão, `http://127.0.0.1:11434` via `.env`).

### Rodando todos os testes

```bash
pytest -q
```

### Rodando apenas o teste do endpoint de chat

```bash
pytest app/tests/test_chat_endpoint.py -q
```

---

## 🧪 Testes manuais via `curl`

### ➗ 1. Multiplicação

```bash
curl -X POST http://localhost:8000/chat   -H "Content-Type: application/json"   -d '{"message": "Quanto é 1234 * 5678?"}'
```

Resposta esperada (exemplo):

```json
{
  "response": "O resultado da multiplicação de 1234 por 5678 é 7.006.652.
"
}
```

---

### √ 2. Raiz quadrada

```bash
curl -X POST http://localhost:8000/chat   -H "Content-Type: application/json"   -d '{"message": "Qual a raiz quadrada de 144?"}'
```

Resposta esperada (exemplo):

```json
{
  "response": "A raiz quadrada de 144 é 12.
"
}
```

---

## 📦 Versionamento e Boas Práticas

O repositório inclui:

- `.gitignore` ignorando:
  - `.venv/`
  - `.env`
  - `__pycache__/`
- `pyproject.toml` com dependências e ferramentas de desenvolvimento
- Arquitetura modular seguindo boas práticas

---

## 🧠 Observações Técnicas

- O agente é carregado **uma única vez** no startup via `lifespan` (arquivo `utils/runtime.py`).
- Logging estruturado com `request_id` por requisição.
- Suporte nativo para novas tools (basta adicionar em `agent/tools.py`).
- Zero dependências em serviços externos de nuvem: o LLM roda 100% local via Ollama.
