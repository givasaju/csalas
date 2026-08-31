# Inventário do Sistema Legado: balcao (ClassSync AI)

Este documento contém o mapeamento e inventário completo da estrutura física do sistema ClassSync AI para engenharia reversa.

---

## 1. Estrutura de Diretórios

A estrutura física do repositório está organizada da seguinte forma:

```
c:/csalas/
├── db/
│   └── migrations.sql
├── src/
│   ├── main.py
│   ├── README.md
│   ├── api/
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── worker.py
│   │       └── static/
│   │           ├── index.css
│   │           └── index.html
│   └── engine/
│       ├── agents.py
│       ├── core.py
│       └── optimization.py
└── tests/
    ├── test_api_csv.py
    ├── test_api_restrictions.py
    ├── test_api_rooms.py
    ├── test_auction.py
    ├── test_building_optimization.py
    ├── test_constraints.py
    └── test_ui_states.py
```

---

## 2. Tecnologias e Frameworks Identificados

*   **Linguagem Principal:** Python 3 (14 arquivos `.py`)
*   **Interface Web:** HTML5 (1 arquivo) e CSS3 (1 arquivo)
*   **Frameworks de Backend:** FastAPI, Uvicorn e Pydantic
*   **Framework de Teste:** Pytest
*   **Gerenciador de Dependências:** `pip` (`requirements.txt`)

---

## 3. Pontos de Entrada

*   **Servidor Backend:** [main.py](file:///c:/csalas/src/main.py)
*   **Roteamento de API:** [routes.py](file:///c:/csalas/src/api/routes.py)
*   **Scaffolding de Testes:** [tests/](file:///c:/csalas/tests/)
*   **Interface Estática:** [index.html](file:///c:/csalas/src/api/static/index.html) e [index.css](file:///c:/csalas/src/api/static/index.css)

---

## 4. Banco de Dados (Superficial)

*   Script DDL inicial de tabelas do leilão e dados prediais: [migrations.sql](file:///c:/csalas/db/migrations.sql)
*   Persistência simulada transacional em memória: [worker.py](file:///c:/csalas/src/api/worker.py)

---

## 5. Cobertura de Testes

*   Suíte de testes integrada baseada em Pytest: 7 arquivos de testes unitários e de integração de rotas e lógicas do motor de alocação de IA.
