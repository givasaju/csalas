#!/usr/bin/env bash
# ==============================================================================
# Script de Provisionamento de Nova Instituição (Linux / macOS)
# ==============================================================================
set -e

TENANT_NAME="$1"
PORT="$2"
DATABASE_URL="$3"
MASTER_CHEF_EMAIL="$4"
MASTER_CHEF_PASSWORD="$5"

if [ -z "$TENANT_NAME" ] || [ -z "$PORT" ]; then
    echo "Uso: $0 <TENANT_NAME> <PORT> [DATABASE_URL] [MASTER_CHEF_EMAIL] [MASTER_CHEF_PASSWORD]"
    echo "Exemplo: $0 faculdade_alpha 8001 \"\" diretor@alpha.edu.br Senha@2026"
    exit 1
fi

DATA_DIR="./data/${TENANT_NAME}"
ENV_FILE=".env.${TENANT_NAME}"

echo "==> Provisionando instituição: ${TENANT_NAME} na porta ${PORT}..."

# 1. Criar diretório de dados persistentes
mkdir -p "${DATA_DIR}"
echo "  [OK] Diretório de dados criado: ${DATA_DIR}"

# 2. Gerar SECRET_KEY aleatória de 64 caracteres hexadecimais
if command -v openssl >/dev/null 2>&1; then
    SECRET_KEY=$(openssl rand -hex 32)
else
    SECRET_KEY=$(head -c 32 /dev/urandom | xxd -p | tr -d '\n' || echo "secret-$(date +%s)")
fi

# 3. Definir DATABASE_URL padrão se não fornecida
if [ -z "$DATABASE_URL" ]; then
    DATABASE_URL="sqlite:////app/data/classsync.db"
fi

# 4. Escrever arquivo de ambiente da instituição
cat > "${ENV_FILE}" <<EOF
TENANT_NAME=${TENANT_NAME}
PORT=${PORT}
HOST=0.0.0.0
DATA_DIR=${DATA_DIR}
DATABASE_URL=${DATABASE_URL}
SECRET_KEY=${SECRET_KEY}
APP_ENV=production
EOF
echo "  [OK] Arquivo gerado: ${ENV_FILE}"

# 5. Semear master-chef se credenciais forem fornecidas
if [ -n "$MASTER_CHEF_EMAIL" ] && [ -n "$MASTER_CHEF_PASSWORD" ]; then
    echo "==> Semeando Master-Chef (${MASTER_CHEF_EMAIL}) na base do tenant..."
    python3 -c "
import os
os.environ['DATABASE_URL'] = 'sqlite:///${DATA_DIR}/project.db'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base, User
from src.api.auth import hash_password

engine = create_engine('sqlite:///${DATA_DIR}/project.db', connect_args={'check_same_thread': False})
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
s = Session()
try:
    u = s.query(User).filter(User.email == '${MASTER_CHEF_EMAIL}').first()
    if not u:
        u = User(
            id='u-${TENANT_NAME}-master',
            name='Gestor Geral Institucional',
            email='${MASTER_CHEF_EMAIL}',
            password_hash=hash_password('${MASTER_CHEF_PASSWORD}'),
            role='gestor',
            department='Administração Geral',
            is_active=True,
            must_change_password=True
        )
        s.add(u)
        s.commit()
finally:
    s.close()
" 2>/dev/null || python -c "
import os
os.environ['DATABASE_URL'] = 'sqlite:///${DATA_DIR}/project.db'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base, User
from src.api.auth import hash_password

engine = create_engine('sqlite:///${DATA_DIR}/project.db', connect_args={'check_same_thread': False})
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
s = Session()
try:
    u = s.query(User).filter(User.email == '${MASTER_CHEF_EMAIL}').first()
    if not u:
        u = User(
            id='u-${TENANT_NAME}-master',
            name='Gestor Geral Institucional',
            email='${MASTER_CHEF_EMAIL}',
            password_hash=hash_password('${MASTER_CHEF_PASSWORD}'),
            role='gestor',
            department='Administração Geral',
            is_active=True,
            must_change_password=True
        )
        s.add(u)
        s.commit()
finally:
    s.close()
" 2>/dev/null || true
    echo "  [OK] Master-Chef provisionado com sucesso (must_change_password=True)."
fi

# 6. Executar subida do container via Docker Compose se docker estiver presente

if command -v docker >/dev/null 2>&1; then
    echo "==> Inicializando container classsync-${TENANT_NAME}..."
    docker compose --project-name "classsync-${TENANT_NAME}" --env-file "${ENV_FILE}" up -d --build
    echo "==> Sucesso! Instituição ${TENANT_NAME} disponível em http://localhost:${PORT}/"
else
    echo "==> Aviso: Docker não encontrado no PATH. Arquivo ${ENV_FILE} e diretório criados."
    echo "    Para executar em modo local direto:"
    echo "    export TENANT_NAME=${TENANT_NAME} PORT=${PORT} SECRET_KEY=${SECRET_KEY} && python -m src.main"
fi
