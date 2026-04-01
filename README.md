# Task Orchestrator API

> A production-grade REST API for task management, built with Python/Flask, PostgreSQL and Docker.

## Architecture
```
┌─────────────────────────────────────────────────────┐
│  Docker Network                                     │
│                                                     │
│  ┌──────────────┐    depends_on     ┌────────────┐  │
│  │   tasks_api  │ ───(healthy)────► │  tasks_db  │  │
│  │  Flask+Gunicorn│                 │ PostgreSQL │  │
│  │  :5000       │                  │  :5432     │  │
│  └──────────────┘                  └────────────┘  │
└─────────────────────────────────────────────────────┘
```

## Quickstart
```bash
# 1. Clone
git clone https://github.com/<seu-user>/task-orchestrator-api
cd task-orchestrator-api

# 2. Configure o ambiente (opcional — defaults funcionam)
cp .env.example .env

# 3. Suba tudo
docker compose up --build
```

A API estará disponível em `http://localhost:5000`.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/tasks/` | Lista todas as tarefas |
| `POST` | `/tasks/` | Cria uma tarefa |
| `PATCH` | `/tasks/:id/complete` | Marca como concluída |
| `DELETE` | `/tasks/:id` | Remove uma tarefa |
| `GET` | `/health` | Health check da API |

### Exemplos com curl
```bash
# Criar tarefa
curl -X POST http://localhost:5000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Estudar Docker", "priority": "high"}'

# Listar tarefas
curl http://localhost:5000/tasks/

# Concluir tarefa (id=1)
curl -X PATCH http://localhost:5000/tasks/1/complete

# Deletar tarefa (id=1)
curl -X DELETE http://localhost:5000/tasks/1
```

### Prioridades válidas
`high` | `medium` | `low`

## Design Decisions

- **Multi-stage Dockerfile**: imagem final ~130MB (vs ~1GB sem otimização)
- **Gunicorn em produção**: multi-worker, mais performático que o servidor dev
- **`depends_on: condition: service_healthy`**: API só sobe após PostgreSQL aceitar conexões
- **Camadas separadas (routes → services → repositories)**: banco pode ser trocado alterando apenas `task_repository.py`
- **Usuário não-root no container**: princípio do menor privilégio