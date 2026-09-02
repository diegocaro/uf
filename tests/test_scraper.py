"""
Tests para el módulo de scraping.
"""

import json
import tempfile
from pathlib import Path

import pandas as pd
import pytest

from uf.scraper import get_uf_data, keep_last_months, merge_uf_data, save_to_json


@pytest.fixture
def html_raw_path():
    html_path = Path("tests", "data", "raw.html")
    assert html_path.exists(), f"El archivo {html_path} no existe"
    return html_path.resolve()


def test_get_uf_data_from_local_file(html_raw_path: Path):
    """
    Test que verifica que se pueden leer los datos de la UF
    desde un archivo HTML local.
    """

    df = get_uf_data(f"file://{html_raw_path}")

    assert set(df.columns) == {"fecha", "valor"}
    assert not df.empty

    assert pd.api.types.is_string_dtype(df["fecha"].dtype)
    assert pd.api.types.is_float_dtype(df["valor"].dtype)

    # Verificar que las fechas tienen el formato correcto (YYYY-MM-DD)
    fecha_pattern = r"^\d{4}-\d{2}-\d{2}$"
    assert df["fecha"].str.match(fecha_pattern).all()


def test_save_to_json():
    """
    Test que verifica que los datos se guardan correctamente
    en formato JSON.
    """
    # Crear un DataFrame de prueba
    data = [
        {"fecha": "2025-01-01", "valor": 38419.17},
        {"fecha": "2025-01-02", "valor": 38421.65},
    ]
    df = pd.DataFrame(data)

    with tempfile.NamedTemporaryFile(delete=True, suffix=".json") as temp_file:
        temp_path = Path(temp_file.name)
        save_to_json(df, "http://test_source", temp_path)
        assert temp_path.exists()

        with temp_path.open() as f:
            json_data = json.load(f)

    # Verificar la estructura del JSON
    assert "data" in json_data
    assert "updated_at" in json_data
    assert "source" in json_data
    assert len(json_data["data"]) == 2

    # Verificar que los datos son correctos
    assert json_data["data"][0]["fecha"] == "2025-01-01"
    assert json_data["data"][0]["valor"] == 38419.17
    assert json_data["data"][1]["fecha"] == "2025-01-02"
    assert json_data["data"][1]["valor"] == 38421.65


def test_merge_uf_data_keeps_previous_days_on_year_change():
    """
    Al cambiar de año, la tabla del sitio solo trae el año nuevo; el merge
    no debe perder los días restantes de diciembre ya guardados.
    """
    existing = pd.DataFrame(
        {
            "fecha": ["2025-12-30", "2025-12-31"],
            "valor": [39020.0, 39030.0],
        }
    )
    new = pd.DataFrame(
        {
            "fecha": ["2026-01-01", "2026-01-02"],
            "valor": [39040.0, 39050.0],
        }
    )

    merged = merge_uf_data(existing, new)

    assert list(merged["fecha"]) == [
        "2025-12-30",
        "2025-12-31",
        "2026-01-01",
        "2026-01-02",
    ]


def test_merge_uf_data_prefers_new_value_on_overlap():
    existing = pd.DataFrame({"fecha": ["2026-01-01"], "valor": [1.0]})
    new = pd.DataFrame({"fecha": ["2026-01-01"], "valor": [2.0]})

    merged = merge_uf_data(existing, new)

    assert len(merged) == 1
    assert merged.iloc[0]["valor"] == 2.0


def test_keep_last_months_discards_older_rows():
    df = pd.DataFrame(
        {
            "fecha": ["2024-01-01", "2025-06-01", "2026-01-01"],
            "valor": [1.0, 2.0, 3.0],
        }
    )

    result = keep_last_months(df, months=12)

    assert list(result["fecha"]) == ["2025-06-01", "2026-01-01"]


def test_compare_with_expected_data():
    """
    Test que compara los datos extraídos con los datos esperados.
    """
    # Ruta al archivo HTML de prueba
    html_path = Path("tests", "data", "raw.html")

    # Ruta al archivo JSON con los datos esperados
    expected_path = Path("tests", "data", "expected.json")

    # Verificar que los archivos existen
    assert html_path.exists(), f"El archivo {html_path} no existe"
    assert expected_path.exists(), f"El archivo {expected_path} no existe"

    # Leer los datos esperados y actuales
    actual_df = get_uf_data(f"file://{html_path.resolve()}")
    with expected_path.open() as f:
        expected_data = json.load(f)
    expected_df = pd.DataFrame(expected_data["data"])

    # Verificar estructura
    assert set(actual_df.columns) == {"fecha", "valor"}
    assert len(actual_df) > 0

    # Comparar los DataFrames completos (ordenados por fecha)
    pd.testing.assert_frame_equal(
        actual_df.sort_values("fecha").reset_index(drop=True),
        expected_df.sort_values("fecha").reset_index(drop=True),
        check_dtype=False,
        atol=0,
    )
