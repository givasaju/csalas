# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Evitar criação de arquivos .pyc e buffer de saída
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    HOST=0.0.0.0 \
    TENANT_NAME=default \
    DATABASE_URL=sqlite:////app/data/classsync.db

WORKDIR /app

# Instalar utilitários básicos e curl para health check
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-privilegiado para segurança
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/data && \
    chown -R appuser:appuser /app

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir sqlalchemy "python-jose[cryptography]"

# Copiar código da aplicação
COPY --chown=appuser:appuser src/ /app/src/

# Alternar para o usuário não-privilegiado
USER appuser

# Porta padrão de escuta do Cloud Run
EXPOSE 8080

# Health check usando a rota de health
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/api/v1/health || exit 1

# Comando com exec para garantir repasse de sinais do sistema (graceful shutdown)
CMD ["sh", "-c", "exec uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
