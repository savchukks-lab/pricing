from datetime import datetime, timezone
from data.demo import PRODUCTS, MARKETS
from domain.cases import CaseType
from services.access_service import can_view, can_edit
from services.audit_service import record


def visible_cases(repo, user):
    return [c for c in repo.cases() if can_view(user, c)]


def save_inputs(repo, case_id, user, changes):
    case = repo.get(case_id)
    if not case or not can_edit(user, case):
        raise PermissionError("Only the owner may edit a draft or returned case.")
    if set(changes) - {"summary", "details", "pricing", "forecast"}:
        raise ValueError("Unsupported input field.")
    case.update(changes)
    case["updated"] = datetime.now(timezone.utc).date().isoformat()
    repo.save(case)
    record(repo, case_id, user, "Inputs saved", case["status"], case["status"])


def create_case(repo, user, name, case_type, product, market, deadline):
    if user not in {"Maya Chen", "Ethan Brooks"}:
        raise PermissionError("Select a case owner to create a case.")
    if not name.strip():
        raise ValueError("Enter a case name.")
    if product not in PRODUCTS or market not in MARKETS:
        raise ValueError("Select a product and market from master data.")
    case_id = f"PMA-{max(int(c['id'].split('-')[1]) for c in repo.cases()) + 1:03}"
    case = {"id": case_id, "name": name.strip(), "type": str(CaseType(case_type)),
            "product": product, "market": market, "owner": user, "status": "Draft",
            "deadline": str(deadline), "updated": datetime.now(timezone.utc).date().isoformat(),
            "revenue_at_risk": 0, "summary": "", "details": {}, "comments": [],
            "pricing": [{"SKU": product, "Currency": "GBP" if market == "United Kingdom" else "EUR", "List price": 0.0, "Discount %": 0.0}],
            "forecast": [{"Measure": "Units", **{f"Y{y}": None for y in range(1, 11)}}]}
    repo.save(case)
    record(repo, case_id, user, "Case created", "", "Draft")
    return case_id


def case_rows(cases):
    return [{"Case ID": c["id"], "Case": c["name"], "Case Type": c["type"],
             "Product": c["product"], "Market": c["market"], "Owner": c["owner"],
             "Status": c["status"], "Deadline": c["deadline"]} for c in cases]
