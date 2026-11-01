"""Small helpers extracted verbatim from AI Decision Platform; see docs/reuse.md."""

import pandas as pd

PERSONAS = {
    "Maya Chen": "KAM North",
    "Ethan Brooks": "KAM South",
    "Jordan Blake": "Sales Manager",
    "Priya Nair": "Pricing Governance Owner",
    "Daniel Ortiz": "Finance Director",
    "Elena Rossi": "Operations Manager",
    "Sarah Morgan": "General Manager",
    "Admin User": "System Administrator",
}

def money(value: float | int | None) -> str:
    if value is None or pd.isna(value):
        return "n/a"
    return f"${float(value):,.0f}"

def pct(value: float | int | None) -> str:
    if value is None or pd.isna(value):
        return "n/a"
    numeric = float(value)
    display_value = numeric * 100 if abs(numeric) <= 1 else numeric
    return f"{display_value:.1f}%"

def safe_float(value: object, default: float = 0.0) -> float:
    if value is None or pd.isna(value):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default
