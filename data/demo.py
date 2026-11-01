"""Fictional data. Dates refer to the explicitly labelled November 2026 snapshot."""
from domain.cases import CaseType

SNAPSHOT = "1 November 2026"
PRODUCTS = ["Avenora 20 mg", "Lumetra 100 mg", "Nexavia 50 mg"]
MARKETS = ["Germany", "France", "United Kingdom"]


def seed_cases():
    names = ["Avenora · annual price review", "Lumetra · hospital tender",
             "Nexavia · payer agreement renewal", "Avenora · hospital exception",
             "Nexavia · launch price proposal", "Lumetra · access expansion"]
    owners = ["Maya Chen", "Ethan Brooks", "Maya Chen", "Ethan Brooks", "Maya Chen", "Maya Chen"]
    statuses = ["Under Review", "Draft", "Changes Requested", "Approved", "Draft", "Under Review"]
    return [{
        "id": f"PMA-{i + 1:03}", "name": names[i], "type": str(kind),
        "product": PRODUCTS[[0, 1, 2, 0, 2, 1][i]], "market": MARKETS[[0, 1, 2, 1, 0, 2][i]], "owner": owners[i],
        "status": statuses[i], "deadline": f"2026-11-{[6, 12, 16, 20, 24, 27][i]:02}",
        "updated": "2026-11-01", "revenue_at_risk": [1200000, 800000, 450000, 0, 0, 650000][i],
        "summary": "Confirm an evidence-backed commercial position while protecting sustainable patient access.",
        "details": {}, "pricing": [{"SKU": PRODUCTS[[0, 1, 2, 0, 2, 1][i]], "Currency": "GBP" if i in {2, 5} else "EUR",
                                    "List price": 120.0, "Discount %": 10.0}],
        "forecast": [{"Measure": "Units", **{f"Y{y}": None for y in range(1, 11)}}],
        "comments": ([{"Author": "Priya Nair", "Comment": "Please update the payer evidence before resubmission."}]
                     if statuses[i] == "Changes Requested" else []),
    } for i, kind in enumerate(CaseType)]


MILESTONES = [
    {"Case ID": "PMA-001", "Workstream": "Pricing", "Milestone": "Evidence review", "Owner": "Maya Chen", "Due": "2026-11-04", "Status": "In progress"},
    {"Case ID": "PMA-002", "Workstream": "Tender", "Milestone": "Bid readiness review", "Owner": "Ethan Brooks", "Due": "2026-11-10", "Status": "At risk"},
    {"Case ID": "PMA-006", "Workstream": "Market Access", "Milestone": "Payer dossier sign-off", "Owner": "Maya Chen", "Due": "2026-11-18", "Status": "Planned"},
]
ACCESS = [{"Case ID": "PMA-006", "Objective": "Expand eligible population", "Pathway": "Payer negotiation", "Stage": "Evidence development", "Next Milestone": "Dossier sign-off · 18 Nov", "Risk": "Evidence gap"}]
TENDERS = [{"Case ID": "PMA-002", "Tender": "Regional hospital supply", "Product": "Lumetra 100 mg", "Market": "France", "Owner": "Ethan Brooks", "Deadline": "2026-11-12", "Stage": "Bid preparation"}]
CONTRACTS = [{"Case ID": "PMA-003", "Counterparty": "Demo payer group", "Product": "Nexavia 50 mg", "Market": "United Kingdom", "Owner": "Maya Chen", "Renewal": "2026-12-31", "Status": "Re-contracting"}]
