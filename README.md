# 📈 UF Scraper

Extrae automáticamente los valores de la **Unidad de Fomento (UF)** desde el sitio web del Banco Central de Chile y genera una elegante página web con un conversor interactivo en tiempo real.

---

## 🚀 Características

* 🔍 **Scraping** de datos actualizado desde el Banco Central usando `pandas` + `lxml`.
* 💾 Guardado de datos en **formato JSON**.
* 🌐 Interfaz web dinámica que carga los valores más recientes automáticamente.
* 🔄 Conversor **UF → CLP** con validación de formato chileno.
* 📋 Opción de **copiar al portapapeles** los resultados del conversor.
* 🧪 **Pruebas automatizadas** con `pytest`.

---

## 🌍 Hosting

> **📡 Hosting listo para producción**
> La carpeta `docs/` está configurada para ser servida directamente mediante **GitHub Pages** (o cualquier otro servicio de hosting estático), permitiendo un acceso web inmediato a los datos y al conversor actualizado. Simplemente *push & deploy*.


---

## 🧰 Requisitos

* Python `3.12+`
* [`uv`](https://github.com/astral-sh/uv) para gestión de dependencias (¡más rápido que pip!)

---

## ⚙️ Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/diegocaro/uf.git
cd uf
```

2. Instala las dependencias:

```bash
uv sync --extra dev
```

---

## 🏃 Uso

Ejecuta el scraper para generar los datos:

```bash
uv run python -m uf.scraper
```

Esto generará:
* 📄 `docs/data/uf.json` — Archivo con los datos actualizados.

También puedes definir una ruta de salida personalizada:

```bash
uv run python -m uf.scraper --output ruta/personalizada/uf.json
```

---

## 🗂️ Estructura del proyecto

```plaintext
uf/
├── uf/              # Código fuente principal
│   └── scraper.py   # Extracción de datos de la UF
├── tests/           # Pruebas con pytest
│   ├── test_scraper.py
│   └── data/        # Fixtures: HTML crudo y JSON esperado
├── docs/            # Sitio web generado
│   ├── index.html
│   └── data/uf.json # Los datos extraídos y procesados
├── pyproject.toml   # Configuración de proyecto
├── uv.lock          # Lockfile de dependencias
└── README.md        # Este documento ✨
```

---

## ✅ Pruebas

Ejecuta los tests con:

```bash
uv run pytest
```

---

## 📄 Licencia

Distribuido bajo licencia **MIT**. Libre para usar, modificar y compartir.

