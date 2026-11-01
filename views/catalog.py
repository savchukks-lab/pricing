"""Top-level skeletons share the same header, navigation, and table components."""
import streamlit as st
from data.demo import ACCESS, TENDERS, CONTRACTS, PRODUCTS, MARKETS
from services.portfolio_service import related
from services.access_service import can_admin
from shared.legacy_helpers import PERSONAS
from ui.components import header, navigation, table, note

PURPOSES = {
    "Prices": "Manage list prices, historical changes and strategic price corridors.",
    "Market Access": "Track access objectives, evidence pathways and payer milestones.",
    "Tenders": "Coordinate bid preparation, ownership and tender deadlines.",
    "Contracts": "Monitor agreements, commercial commitments and renewal decisions.",
    "Intelligence": "Bring external evidence into pricing and access decisions.",
    "Insights": "Review portfolio performance, exposure and decision trends.",
    "Admin": "Maintain users, master data and decision governance.",
}
SECTIONS = {
    "Prices": ("Current Prices", "Price History", "Price Corridors"),
    "Intelligence": ("Competitors", "External Prices", "Reimbursement / HTA", "IRP", "Policy"),
    "Admin": ("Users", "Roles", "Products", "Markets", "Approval Rules", "Workflows", "Master Data", "Integrations", "Audit"),
}


def render(repo, user, cases, page):
    header(page, PURPOSES[page])
    if page == "Admin" and not can_admin(user):
        note("Select Admin User in the demo identity menu to inspect administration.")
        return
    sections = SECTIONS.get(page)
    section = st.query_params.get("section", "")
    if sections:
        section = section if section in sections else sections[0]
        from ui.components import navigate
        navigation(sections, section, "section-nav", lambda s: navigate(page, section=s))
        st.subheader(section)
    if page == "Prices":
        if section == "Current Prices":
            table([{"Product": c["product"], "Market": c["market"], "Currency": c["pricing"][0]["Currency"], "Demo list price": c["pricing"][0]["List price"], "Source": "Case input · not approved master price"} for c in cases])
        else:
            note("Price history and approved corridors will be connected to governed master data.")
            table([], ["Product", "Market", "Effective date", "Source", "Approved price" if section == "Price History" else "Floor / Target / Ceiling"])
    elif page in {"Market Access", "Tenders", "Contracts"}:
        rows = {"Market Access": ACCESS, "Tenders": TENDERS, "Contracts": CONTRACTS}[page]
        table(related(rows, cases), list(rows[0]))
        st.subheader({"Market Access": "Evidence & readiness", "Tenders": "Bid readiness", "Contracts": "Obligations & renewals"}[page])
        note("Workstream ownership, milestones and actions will support this portfolio. Demo records are illustrative.")
    elif page == "Intelligence":
        table([], {"Competitors": ["Product", "Competitor", "Market", "Evidence date", "Source"],
                   "External Prices": ["Product", "Market", "Price", "Currency", "Source", "As of"],
                   "Reimbursement / HTA": ["Product", "Market", "Agency", "Decision", "Source"],
                   "IRP": ["Market", "Reference basket", "Rule", "Review date"],
                   "Policy": ["Market", "Policy", "Effective date", "Source"]}[section])
        note("No live external feeds are connected. Evidence requires source and date validation.")
    elif page == "Insights":
        st.subheader("Decision pipeline")
        statuses = sorted({c["status"] for c in cases})
        table([{"Status": status, "Cases": sum(c["status"] == status for c in cases)} for status in statuses])
        st.subheader("Commercial & access analytics")
        table([{"Analysis": a, "Status": "Planned", "Required inputs": b} for a,b in [
            ("Price realization", "Approved price and volume history"),
            ("Access progress", "Milestone completion and population coverage"),
            ("Exposure by market", "Validated revenue and currency assumptions")]])
    elif page == "Admin":
        if section == "Users":
            table([{"User": name, "Role": role, "Identity source": "Demo persona"} for name,role in PERSONAS.items()])
        elif section == "Roles":
            table([{"Role": "Case owner", "Visibility": "Owned cases", "Actions": "Create, edit, submit, resubmit"},
                   {"Role": "Independent reviewer", "Visibility": "All demo cases", "Actions": "Approve, request changes, reject"},
                   {"Role": "System Administrator", "Visibility": "All demo cases and administration", "Actions": "Inspect configuration and audit"}])
        elif section in {"Products", "Markets"}:
            table([{section[:-1]: value} for value in (PRODUCTS if section == "Products" else MARKETS)])
        elif section == "Audit":
            table(list(reversed(repo.audit())))
        elif section == "Integrations":
            table([{"Integration": name, "Status": "Not connected"} for name in ["SAP", "Salesforce", "Azure SSO", "External pricing feeds", "AI service (optional)"]])
        elif section in {"Approval Rules", "Workflows"}:
            table([{"From": "Draft / Changes Requested", "Action": "Submit / Resubmit", "To": "Under Review", "Actor": "Owner"},
                   {"From": "Under Review", "Action": "Approve / Request Changes / Reject", "To": "Approved / Changes Requested / Rejected", "Actor": "Independent reviewer"}])
            note("Demo uses one independent review. Multi-step approval routing is a future service extension.")
        else:
            table([], ["Entity", "Code", "Description", "Effective date", "Owner"])
