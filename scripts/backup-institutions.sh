#!/usr/bin/env bash
# ==============================================================================
# Script de Backup Centralizado dos Volumes Multi-Tenant (Linux / macOS)
# ==============================================================================
set -e

BACKUP_DIR="${1:-./backups}"
DATA_ROOT="./data"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

mkdir -p "${BACKUP_DIR}"
echo "==> Iniciando backup centralizado de instituições em ${BACKUP_DIR}..."

if [ ! -d "${DATA_ROOT}" ]; then
    echo "Diretório de dados ${DATA_ROOT} não encontrado."
    exit 0
fi

for tenant_dir in "${DATA_ROOT}"/*; do
    if [ -d "${tenant_dir}" ]; then
        tenant_name=$(basename "${tenant_dir}")
        archive_name="${BACKUP_DIR}/backup_${tenant_name}_${TIMESTAMP}.tar.gz"
        echo "  -> Compactando dados da instituição: ${tenant_name}..."
        tar -czf "${archive_name}" -C "${DATA_ROOT}" "${tenant_name}"
        echo "     [OK] Criado: ${archive_name} ($(du -h "${archive_name}" 2>/dev/null | cut -f1 || echo ''))"
    fi
done

echo "==> Rotina de backup concluída com sucesso!"
