"""Illustrative arithmetic only. No IRP, tax, rebate waterfall or access engine."""
import math
from shared.legacy_helpers import safe_float


def price_outputs(rows):
    output = []
    for row in rows:
        price, discount = safe_float(row["List price"]), safe_float(row["Discount %"])
        if not math.isfinite(price) or not math.isfinite(discount) or price < 0 or not 0 <= discount <= 100:
            raise ValueError("Use a non-negative list price and a discount between 0 and 100%.")
        output.append({**row, "Illustrative net price": round(price * (1 - discount / 100), 2)})
    return output
