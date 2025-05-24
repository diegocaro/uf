"""
Módulo para escrapear los valores de la UF desde el Banco Central de Chile.
Utiliza pandas para extraer los datos de las tablas HTML.
"""

import json
import logging
from datetime import datetime

import pandas as pd

DEFAULT_URL = "https://si3.bcentral.cl/Siete/ES/Siete/Cuadro/CAP_PRECIOS/MN_CAP_PRECIOS/UF_IVP_DIARIO/UF_IVP_DIARIO"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_date(date_str: str) -> str:
    """
    Convierte una fecha del formato DD.MMM.YYYY a YYYY-MM-DD.
    """
    month_map = {
        "ene": "01",
        "feb": "02",
        "mar": "03",
        "abr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "ago": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dic": "12",
    }

    parts = date_str.split(".")
    if len(parts) != 3:
        raise ValueError(
            f"Formato de fecha inválido: {date_str}. Se esperaba DD.MMM.YYYY"
        )

    day, month_abbr, year = parts
    month = month_map.get(month_abbr.lower())
    if month is None:
        raise ValueError(f"Mes inválido: {month_abbr}. Se esperaba mes abreviado")
    return f"{year}-{month}-{day.zfill(2)}"


def parse_value(value: str) -> float:
    return float(value.replace(".", "").replace(",", "."))


def transform_uf_table(table: pd.DataFrame) -> pd.DataFrame:
    uf_table = table[table["Serie"].astype(str).str.contains("Unidad de fomento", case=False, na=False)]  # type: ignore
    if uf_table.empty:  # type: ignore
        return pd.DataFrame(columns=["fecha", "valor"])

    date_cols = [col for col in uf_table.columns if col not in ["Serie", "Sel."]]
    df = uf_table[date_cols].T.reset_index()
    df.columns = ["fecha", "valor"]

    df["fecha"] = df["fecha"].astype(str).apply(parse_date)
    df["valor"] = df["valor"].astype(str).apply(parse_value)

    return df.sort_values("fecha", ignore_index=True)


def get_uf_data(url: str = DEFAULT_URL) -> pd.DataFrame:
    tables = [t for t in pd.read_html(url) if "Serie" in t.columns]  # type: ignore

    for table in tables:
        df = transform_uf_table(table)
        if not df.empty:
            return df

    raise ValueError("No se encontró la tabla de UF en la página.")


def save_to_json(df: pd.DataFrame, source: str, output_path: str) -> None:
    data = {
        "data": df.to_dict(orient="records"),  # type: ignore
        "updated_at": datetime.now().astimezone().isoformat(),
        "source": source,
    }
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Datos guardados en {output_path} desde {source}")


def retrieve_data(output_path: str):
    """Obtiene datos de la UF y los guarda en un archivo JSON."""
    save_to_json(get_uf_data(), DEFAULT_URL, output_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scrapear datos de la UF.")
    parser.add_argument(
        "--output",
        type=str,
        default="docs/data/uf.json",
        help="Ruta del archivo de salida JSON.",
    )

    retrieve_data(parser.parse_args().output)
