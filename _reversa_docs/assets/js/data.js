window.RV_DATA = {
  "modules": {
    "modules": [
      {
        "id": "src\\database.py",
        "name": "database.py",
        "path": "src\\database.py",
        "loc": 111,
        "complexity": 13,
        "type": "data",
        "language": "python"
      },
      {
        "id": "src\\main.py",
        "name": "main.py",
        "path": "src\\main.py",
        "loc": 24,
        "complexity": 4,
        "type": "entrypoint",
        "language": "python"
      },
      {
        "id": "src\\models.py",
        "name": "models.py",
        "path": "src\\models.py",
        "loc": 112,
        "complexity": 3,
        "type": "data",
        "language": "python"
      },
      {
        "id": "src\\__init__.py",
        "name": "__init__.py",
        "path": "src\\__init__.py",
        "loc": 0,
        "complexity": 1,
        "type": "module",
        "language": "python"
      },
      {
        "id": "src\\api\\allocation_validator.py",
        "name": "allocation_validator.py",
        "path": "src\\api\\allocation_validator.py",
        "loc": 27,
        "complexity": 7,
        "type": "api",
        "language": "python"
      },
      {
        "id": "src\\api\\auth.py",
        "name": "auth.py",
        "path": "src\\api\\auth.py",
        "loc": 43,
        "complexity": 7,
        "type": "api",
        "language": "python"
      },
      {
        "id": "src\\api\\reports.py",
        "name": "reports.py",
        "path": "src\\api\\reports.py",
        "loc": 895,
        "complexity": 99,
        "type": "api",
        "language": "python"
      },
      {
        "id": "src\\api\\routes.py",
        "name": "routes.py",
        "path": "src\\api\\routes.py",
        "loc": 1529,
        "complexity": 233,
        "type": "api",
        "language": "python"
      },
      {
        "id": "src\\api\\schemas.py",
        "name": "schemas.py",
        "path": "src\\api\\schemas.py",
        "loc": 149,
        "complexity": 2,
        "type": "api",
        "language": "python"
      },
      {
        "id": "src\\api\\worker.py",
        "name": "worker.py",
        "path": "src\\api\\worker.py",
        "loc": 146,
        "complexity": 22,
        "type": "api",
        "language": "python"
      },
      {
        "id": "src\\engine\\agents.py",
        "name": "agents.py",
        "path": "src\\engine\\agents.py",
        "loc": 85,
        "complexity": 13,
        "type": "core-engine",
        "language": "python"
      },
      {
        "id": "src\\engine\\core.py",
        "name": "core.py",
        "path": "src\\engine\\core.py",
        "loc": 358,
        "complexity": 72,
        "type": "core-engine",
        "language": "python"
      },
      {
        "id": "src\\engine\\optimization.py",
        "name": "optimization.py",
        "path": "src\\engine\\optimization.py",
        "loc": 133,
        "complexity": 49,
        "type": "core-engine",
        "language": "python"
      }
    ]
  },
  "deps": {
    "edges": [
      {
        "source": "src\\database.py",
        "target": "sqlalchemy",
        "type": "import"
      },
      {
        "source": "src\\database.py",
        "target": "sqlalchemy.orm",
        "type": "import"
      },
      {
        "source": "src\\database.py",
        "target": "src.models",
        "type": "import"
      },
      {
        "source": "src\\database.py",
        "target": "os",
        "type": "import"
      },
      {
        "source": "src\\database.py",
        "target": "sqlalchemy",
        "type": "import"
      },
      {
        "source": "src\\database.py",
        "target": "json",
        "type": "import"
      },
      {
        "source": "src\\database.py",
        "target": "src.models",
        "type": "import"
      },
      {
        "source": "src\\main.py",
        "target": "os",
        "type": "import"
      },
      {
        "source": "src\\main.py",
        "target": "uvicorn",
        "type": "import"
      },
      {
        "source": "src\\main.py",
        "target": "fastapi",
        "type": "import"
      },
      {
        "source": "src\\main.py",
        "target": "fastapi.responses",
        "type": "import"
      },
      {
        "source": "src\\main.py",
        "target": "src.api.routes",
        "type": "import"
      },
      {
        "source": "src\\models.py",
        "target": "sqlalchemy",
        "type": "import"
      },
      {
        "source": "src\\models.py",
        "target": "enum",
        "type": "import"
      },
      {
        "source": "src\\models.py",
        "target": "sqlalchemy.orm",
        "type": "import"
      },
      {
        "source": "src\\models.py",
        "target": "datetime",
        "type": "import"
      },
      {
        "source": "src\\api\\allocation_validator.py",
        "target": "typing",
        "type": "import"
      },
      {
        "source": "src\\api\\auth.py",
        "target": "fastapi",
        "type": "import"
      },
      {
        "source": "src\\api\\auth.py",
        "target": "fastapi.security",
        "type": "import"
      },
      {
        "source": "src\\api\\auth.py",
        "target": "jose",
        "type": "import"
      },
      {
        "source": "src\\api\\auth.py",
        "target": "pydantic",
        "type": "import"
      },
      {
        "source": "src\\api\\reports.py",
        "target": "io",
        "type": "import"
      },
      {
        "source": "src\\api\\reports.py",
        "target": "datetime",
        "type": "import"
      },
      {
        "source": "src\\api\\reports.py",
        "target": "typing",
        "type": "import"
      },
      {
        "source": "src\\api\\reports.py",
        "target": "reportlab.lib.pagesizes",
        "type": "import"
      },
      {
        "source": "src\\api\\reports.py",
        "target": "reportlab.platypus",
        "type": "import"
      },
      {
        "source": "src\\api\\reports.py",
        "target": "reportlab.lib.styles",
        "type": "import"
      },
      {
        "source": "src\\api\\reports.py",
        "target": "reportlab.lib",
        "type": "import"
      },
      {
        "source": "src\\api\\reports.py",
        "target": "openpyxl",
        "type": "import"
      },
      {
        "source": "src\\api\\reports.py",
        "target": "openpyxl.styles",
        "type": "import"
      },
      {
        "source": "src\\api\\reports.py",
        "target": "openpyxl.utils",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "csv",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "uuid",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "logging",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "datetime",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "io",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "fastapi",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "sqlalchemy.orm",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "sqlalchemy.orm.attributes",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "typing",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "src.api.schemas",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "src.api.allocation_validator",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "src.database",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "src",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "src.api.worker",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "src.engine.core",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "os",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "fastapi.responses",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "src.api.reports",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "json",
        "type": "import"
      },
      {
        "source": "src\\api\\routes.py",
        "target": "json",
        "type": "import"
      },
      {
        "source": "src\\api\\schemas.py",
        "target": "pydantic",
        "type": "import"
      },
      {
        "source": "src\\api\\schemas.py",
        "target": "typing",
        "type": "import"
      },
      {
        "source": "src\\api\\schemas.py",
        "target": "typing",
        "type": "import"
      },
      {
        "source": "src\\api\\worker.py",
        "target": "uuid",
        "type": "import"
      },
      {
        "source": "src\\api\\worker.py",
        "target": "time",
        "type": "import"
      },
      {
        "source": "src\\api\\worker.py",
        "target": "logging",
        "type": "import"
      },
      {
        "source": "src\\api\\worker.py",
        "target": "concurrent.futures",
        "type": "import"
      },
      {
        "source": "src\\api\\worker.py",
        "target": "typing",
        "type": "import"
      },
      {
        "source": "src\\api\\worker.py",
        "target": "src.engine.core",
        "type": "import"
      },
      {
        "source": "src\\api\\worker.py",
        "target": "src",
        "type": "import"
      },
      {
        "source": "src\\api\\worker.py",
        "target": "src.database",
        "type": "import"
      },
      {
        "source": "src\\engine\\agents.py",
        "target": "logging",
        "type": "import"
      },
      {
        "source": "src\\engine\\agents.py",
        "target": "typing",
        "type": "import"
      },
      {
        "source": "src\\engine\\core.py",
        "target": "logging",
        "type": "import"
      },
      {
        "source": "src\\engine\\core.py",
        "target": "collections",
        "type": "import"
      },
      {
        "source": "src\\engine\\core.py",
        "target": "typing",
        "type": "import"
      },
      {
        "source": "src\\engine\\core.py",
        "target": "src.engine.agents",
        "type": "import"
      },
      {
        "source": "src\\engine\\core.py",
        "target": "src.engine.optimization",
        "type": "import"
      },
      {
        "source": "src\\engine\\core.py",
        "target": "src.api.allocation_validator",
        "type": "import"
      },
      {
        "source": "src\\engine\\optimization.py",
        "target": "logging",
        "type": "import"
      },
      {
        "source": "src\\engine\\optimization.py",
        "target": "typing",
        "type": "import"
      }
    ],
    "cycles": []
  },
  "metrics": {
    "schemaVersion": 1,
    "generatedAt": "2026-08-17T08:38:00Z",
    "treemap_loc_by_folder": [
      {
        "folder": "src",
        "loc": 247,
        "modules": 4
      },
      {
        "folder": "src\\api",
        "loc": 2789,
        "modules": 6
      },
      {
        "folder": "src\\engine",
        "loc": 576,
        "modules": 3
      }
    ],
    "top_complexity": [
      {
        "name": "routes.py",
        "complexity": 233,
        "loc": 1529
      },
      {
        "name": "reports.py",
        "complexity": 99,
        "loc": 895
      },
      {
        "name": "core.py",
        "complexity": 72,
        "loc": 358
      },
      {
        "name": "optimization.py",
        "complexity": 49,
        "loc": 133
      },
      {
        "name": "worker.py",
        "complexity": 22,
        "loc": 146
      },
      {
        "name": "database.py",
        "complexity": 13,
        "loc": 111
      },
      {
        "name": "agents.py",
        "complexity": 13,
        "loc": 85
      },
      {
        "name": "allocation_validator.py",
        "complexity": 7,
        "loc": 27
      },
      {
        "name": "auth.py",
        "complexity": 7,
        "loc": 43
      },
      {
        "name": "main.py",
        "complexity": 4,
        "loc": 24
      }
    ],
    "loc_histogram": {
      "bins": [
        "0-50",
        "51-100",
        "101-200",
        "201-500",
        "500+"
      ],
      "counts": [
        4,
        1,
        5,
        1,
        2
      ]
    },
    "language_distribution": [
      {
        "language": "python",
        "modules": 13,
        "loc": 3612
      }
    ]
  },
  "glossary": {
    "projectName": "ClassSync AI",
    "tagline": "Motor de Otimiza\u00e7\u00e3o e Distribui\u00e7\u00e3o de Salas de Aula com Intelig\u00eancia Artificial",
    "concepts": [
      {
        "term": "AAC",
        "definition": "Aloca\u00e7\u00e3o Inicial considerando capacidade f\u00edsica, acessibilidade e recursos."
      },
      {
        "term": "ACC + AMR",
        "definition": "Resolu\u00e7\u00e3o de Conflitos via leil\u00e3o cooperativo fechado com sistema de cr\u00e9ditos."
      },
      {
        "term": "BuildingOptimizer",
        "definition": "Otimizador Energ\u00e9tico que consolida turmas para fechar blocos prediais subutilizados."
      },
      {
        "term": "Restri\u00e7\u00f5es Hor\u00e1rias",
        "definition": "Indisponibilidades cadastradas pelos docentes para evitar choques de hor\u00e1rio."
      }
    ]
  },
  "featuresIndex": {
    "specs": [
      {
        "id": "gerenciador-espacos",
        "name": "Gerenciador Espacos",
        "slug": "gerenciador-espacos"
      },
      {
        "id": "motor-alocacao",
        "name": "Motor Alocacao",
        "slug": "motor-alocacao"
      },
      {
        "id": "painel-ocupacao",
        "name": "Painel Ocupacao",
        "slug": "painel-ocupacao"
      }
    ]
  },
  "sealSvg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 800 800\" width=\"100%\" height=\"100%\"><rect width=\"800\" height=\"800\" fill=\"#0f172a\" rx=\"40\"/><circle cx=\"400\" cy=\"400\" r=\"300\" fill=\"none\" stroke=\"#6366f1\" stroke-width=\"4\" stroke-dasharray=\"12 12\"/><circle cx=\"400\" cy=\"400\" r=\"200\" fill=\"none\" stroke=\"#3b82f6\" stroke-width=\"3\"/><polygon points=\"400,220 520,490 280,490\" fill=\"none\" stroke=\"#10b981\" stroke-width=\"4\"/><text x=\"400\" y=\"410\" text-anchor=\"middle\" fill=\"#f8fafc\" font-family=\"sans-serif\" font-size=\"28\" font-weight=\"bold\">CLASSSYNC AI</text></svg>",
  "sealMiniSvg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 64 64\" width=\"32\" height=\"32\"><circle cx=\"32\" cy=\"32\" r=\"28\" fill=\"#1e293b\" stroke=\"#6366f1\" stroke-width=\"3\"/><text x=\"32\" y=\"37\" text-anchor=\"middle\" fill=\"#6366f1\" font-family=\"sans-serif\" font-size=\"14\" font-weight=\"bold\">CS</text></svg>",
  "seedShort": "balcao26",
  "nav": [
    {
      "id": "index",
      "href": "index.html",
      "label": "Vis\u00e3o Geral"
    },
    {
      "id": "manual-usuario",
      "href": "manual-usuario.html",
      "label": "Manual do Usu\u00e1rio"
    },
    {
      "id": "arquitetura",
      "href": "arquitetura.html",
      "label": "Arquitetura 3D"
    },
    {
      "id": "modulos",
      "href": "modulos.html",
      "label": "M\u00f3dulos"
    },
    {
      "id": "topologia",
      "href": "topologia.html",
      "label": "Topologia"
    },
    {
      "id": "metricas",
      "href": "metricas.html",
      "label": "M\u00e9tricas"
    },
    {
      "id": "glossario",
      "href": "glossario.html",
      "label": "Gloss\u00e1rio"
    },
    {
      "id": "deck",
      "href": "deck.html",
      "label": "Deck"
    }
  ]
};
