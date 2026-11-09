"""Lógica compartida con notebooks/superstore-data-analysis.ipynb.

El notebook y la interfaz Reflex llaman a la misma función pura de filtrado.
"""
from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "superstore.csv"


def load_superstore() -> pd.DataFrame:
    frame = pd.read_csv(DATA_PATH, encoding="ISO-8859-1", dtype={"Postal Code": str})
    frame.columns = frame.columns.str.strip().str.replace(" ", "_").str.lower()
    for column in ["order_date", "ship_date"]:
        frame[column] = pd.to_datetime(frame[column], format="%m/%d/%Y", errors="raise")
    frame["postal_code"] = frame["postal_code"].fillna("").astype(str)
    return frame


def filtrar_superstore(base, config):
    result = base.copy()
    for column, chosen in config.get('categorias', {}).items():
        if chosen:
            result = result.loc[result[column].isin(chosen)]
    for column, (minimum, maximum) in config.get('rangos', {}).items():
        result = result.loc[result[column].between(minimum, maximum)]
    for column, (start, end) in config.get('fechas', {}).items():
        if start is not None:
            result = result.loc[result[column].dt.date >= start]
        if end is not None:
            result = result.loc[result[column].dt.date <= end]
    for column, text in config.get('textos', {}).items():
        if text.strip():
            result = result.loc[result[column].astype(str).str.contains(text.strip(), case=False, regex=False, na=False)]
    for key, values, series in [
        ('años', config.get('años', []), result['order_date'].dt.year),
        ('meses', config.get('meses', []), result['order_date'].dt.month),
        ('dias', config.get('dias', []), result['order_date'].dt.dayofweek),
    ]:
        if values:
            result = result.loc[series.reindex(result.index).isin(values)]
    status = config.get('rentabilidad', 'Todas')
    if status == 'Con beneficio': result = result.loc[result['profit'] > 0]
    if status == 'Con pérdidas': result = result.loc[result['profit'] < 0]
    if status == 'Sin beneficio ni pérdida': result = result.loc[result['profit'] == 0]
    if config.get('sin_descuento'): result = result.loc[result['discount'] == 0]
    if config.get('limite_5000'): result = result.loc[result['sales'] < 5000]
    if config.get('quitar_duplicados'): result = result.drop_duplicates()
    return result.copy()
