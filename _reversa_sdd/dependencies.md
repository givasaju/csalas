# Dependências do Sistema: balcao (ClassSync AI)

Este documento lista todas as dependências críticas do ClassSync AI mapeadas pelo Scout.

---

## 1. Dependências do Python

| Biblioteca | Versão Declarada | Origem | Papel no Sistema |
|------------|------------------|--------|------------------|
| `fastapi` | `>=0.110.0` | `requirements.txt` | Core do framework REST API para rotas HTTP de controle e dados. |
| `uvicorn` | `>=0.15.0` | `requirements.txt` | Servidor web ASGI assíncrono para execução do FastAPI local. |
| `pydantic` | `>=2.0.0` | `requirements.txt` | Validação de tipos e segurança estrutural de payloads de entrada das APIs. |
| `pytest` | `>=8.0.0` | `requirements.txt` | Framework de testes unitários e de integração de rotas e classes de IA. |
| `python-multipart` | `>=0.0.9` | `requirements.txt` | Parser multipart obrigatório para suportar upload de arquivos CSV de salas. |
| `httpx` | `>=0.20.0` | `requirements.txt` | Cliente HTTP assíncrono utilizado no TestClient do FastAPI nos testes integrados. |

---

## 2. Bibliotecas de Frontend

*   **Google Fonts Inter:** Utilizada via importação de folha de estilos externa no `index.html` para tipografia de alta fidelidade e design responsivo.
