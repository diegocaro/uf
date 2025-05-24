"""
Tests para el módulo de scraping.
"""

import json
import os
import tempfile

import pandas as pd
import pytest

from uf.scraper import get_uf_data, save_to_json


@pytest.fixture
def html_raw_path():
    html_path = os.path.join("tests", "data", "raw.html")
    assert os.path.exists(html_path), f"El archivo {html_path} no existe"
    return os.path.abspath(html_path)


def test_get_uf_data_from_local_file(html_raw_path: str):
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
        temp_path = temp_file.name
        save_to_json(df, "http://test_source", temp_path)
        assert os.path.exists(temp_path)

        with open(temp_path, "r") as f:
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


def test_compare_with_expected_data():
    """
    Test que compara los datos extraídos con los datos esperados.
    """
    # Ruta al archivo HTML de prueba
    html_path = os.path.join("tests", "data", "raw.html")

    # Ruta al archivo JSON con los datos esperados
    expected_path = os.path.join("tests", "data", "expected.json")

    # Verificar que los archivos existen
    assert os.path.exists(html_path), f"El archivo {html_path} no existe"
    assert os.path.exists(expected_path), f"El archivo {expected_path} no existe"

    # Leer los datos esperados y actuales
    actual_df = get_uf_data(f"file://{os.path.abspath(html_path)}")
    with open(expected_path, "r") as f:
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
