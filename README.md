# UF Scraper

Este proyecto extrae los valores de la Unidad de Fomento (UF) desde el sitio web del Banco Central de Chile y los muestra en una página web estática.

## Características

- Extracción de datos de la UF directamente desde el Banco Central usando pandas.
- Guardado de datos en formato JSON.
- Generación de una página web estática con los valores de la UF.
- Pruebas automatizadas con pytest.

## Requisitos

- Python 3.10 o superior
- uv (para gestión de dependencias)

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/tu-usuario/uf-scraper.git
cd uf-scraper
```

2. Instala las dependencias con uv:
```bash
uv pip install -e ".[dev]"
```

## Uso

Para ejecutar el scraper y generar la página web:

```bash
python main.py
```

Esto creará:
- Un archivo JSON con los datos en `data/uf.json`
- Una página web estática en `index.html`

## Estructura del proyecto

```
uf/
├── data/            # Directorio para almacenar los datos extraídos
├── src/             # Código fuente
│   ├── __init__.py
│   ├── scraper.py   # Módulo para extraer datos
│   └── web.py       # Módulo para generar la página web
│   └── templates/   # Plantillas HTML
│       └── uf_template.html # Plantilla para la página web
├── tests/           # Pruebas automatizadas
│   ├── __init__.py
│   ├── test_scraper.py
│   ├── test_web.py
│   └── data/        # Datos de prueba
│       ├── expected.json
│       └── raw.html
├── main.py          # Script principal
├── pyproject.toml   # Configuración del proyecto
└── README.md        # Este archivo
```

## Pruebas

Para ejecutar las pruebas:

```bash
pytest
```

## Licencia

MIT

## Pruebas

Para ejecutar las pruebas:

```bash
pytest
```

## Licencia

MIT
