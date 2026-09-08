# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Evitar criação de arquivos .pyc e buffer de saída
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    HOST=0.0.0.0 \
    TENANT_NAME=default \
    DATABASE_URL=sqlite:////app/data/classsync.db

WORKDIR /app

# Instalar utilitários básicos e curl para health check
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir sqlalchemy python-jose[cryptography]

# Criar pasta para volume persistente de dados
RUN mkdir -p /app/data

# Copiar código da aplicação
COPY src/ /app/src/

# Expor porta
EXPOSE 8000

# Health check usando a rota de health
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/api/v1/health || exit 1

# Comando padrão de inicialização
CMD ["sh", "-c", "uvicorn src.main:app --host ${HOST} --port ${PORT}"]
