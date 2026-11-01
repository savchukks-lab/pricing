"""Case definitions are independent of Streamlit and storage."""
from enum import StrEnum


class CaseType(StrEnum):
    PRICE_CHANGE = "Price Change"
    TENDER = "Tender Bid"
    CONTRACT = "Contract / Re-contracting"
    EXCEPTION = "Discount / Pricing Exception"
    LAUNCH = "Launch Price"
    ACCESS = "Net Price / Access Proposal"


CASE_SECTIONS = (
    "Overview", "Pricing", "Market & Competition", "Forecast", "Market Access",
    "Contracting", "Financial Impact", "Governance", "Decision Case",
)
# Configuration, rather than branches throughout the pages, controls applicability.
CASE_SCHEMAS = {
    kind: {
        "sections": tuple(s for s in CASE_SECTIONS if not (
            s == "Contracting" and kind in {CaseType.PRICE_CHANGE, CaseType.LAUNCH}
        )),
        "fields": {
            CaseType.PRICE_CHANGE: ("Effective date", "Reason for change"),
            CaseType.TENDER: ("Tender reference", "Bid deadline"),
            CaseType.CONTRACT: ("Counterparty", "Renewal date"),
            CaseType.EXCEPTION: ("Exception rationale", "Validity end date"),
            CaseType.LAUNCH: ("Launch date", "Reference market"),
            CaseType.ACCESS: ("Access objective", "Reimbursement pathway"),
        }[kind],
    } for kind in CaseType
}


def sections_for(case_type: str) -> tuple[str, ...]:
    return CASE_SCHEMAS[CaseType(case_type)]["sections"]
