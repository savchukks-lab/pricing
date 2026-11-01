from engine.pricing import price_outputs
from services.case_service import save_inputs


def save_pricing(repo, case_id, user, rows):
    price_outputs(rows)  # Validate at the service boundary, not only in widgets.
    save_inputs(repo, case_id, user, {"pricing": rows})
