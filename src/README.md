# ClassSync AI - Core Allocation Engine, Space Manager & Dashboard

Este repositório contém o subsistema completo do ClassSync AI.

---

## 1. Módulo `core-allocation-engine`

O motor orquestra as seguintes fases:
1.  **Alocação Inicial (AAC):** Valida de forma estrita as restrições mandatórias de capacidade física, acessibilidade e recursos.
2.  **Resolução de Conflitos (ACC + AMR):** Arbitragem via leilão cooperativo fechado onde coordenações utilizam créditos (iniciados com 1000 créditos) para desempatar grades, recebendo compensações ao perder disputas.
3.  **Otimização Energética (BuildingOptimizer):** Consolida turmas de blocos subutilizados (ocupação < 20%) para blocos mais densamente povoados, sinalizando o fechamento predial.

---

## 2. Módulo `academic-space-manager`

Este módulo expõe as APIs HTTP de gerenciamento de inventário físico, cadastro de professores e restrições.
*   **POST** `/api/v1/rooms`: Cadastro de sala de aula física (valida capacidade > 0).
*   **POST** `/api/v1/rooms/import-csv`: Importação transacional "Tudo ou Nada" de salas.
*   **POST** `/api/v1/allocation/restrictions`: Cadastro de indisponibilidades docentes.
*   **DELETE** `/api/v1/allocation/restrictions`: Reset semestral das restrições horárias.
*   **GET** `/api/v1/allocation/input-data`: Payload unificado de insumos da IA.

---

## 3. Módulo `occupancy-dashboard`

Uma interface interativa SPA (Single Page Application) servida diretamente pelo FastAPI.

### Funcionalidades Visuais
*   **KPI Cards:** Exibição dinâmica de métricas chaves de Ocupação Geral, Economia de Energia, Blocos Desativados e Conflitos Resolvidos.
*   **Controle de Execução:** Botão interativo para disparar a otimização de alocação de IA em lote, mostrando barra de progresso e status assíncrono em tempo real.
*   **Auditoria de Leilões:** Extrato de transações de créditos detalhando as compensações pagas e recebidas pelas coordenações.

### Inicialização e Acesso
As rotas de servir a interface estática estão configuradas no entrypoint da aplicação:
*   Acesse **`http://localhost:8000/`** no navegador para abrir a interface gráfica.
*   Os arquivos estáticos correspondentes residem em `src/api/static/`.
