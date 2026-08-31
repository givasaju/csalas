# Use a imagem base oficial do Python (versão slim para menor tamanho da imagem)
FROM python:3.11-slim

# Configurações de ambiente para otimizar a execução do Python em containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Define o PYTHONPATH para incluir a raiz do projeto (/app)
ENV PYTHONPATH=/app

# Instala pacotes do sistema necessários para compilações leves (se necessário)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências Python (utiliza cache de camadas do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte da aplicação para o container
COPY . .

# Garante que a pasta do banco de dados exista
RUN mkdir -p db

# Porta exposta padrão (o Google Cloud Run injeta sua própria variável PORT dinamicamente)
EXPOSE 8080

# Comando de inicialização configurado para aceitar a variável $PORT do Cloud Run
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
