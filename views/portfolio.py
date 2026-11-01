import streamlit as st
from data.demo import MILESTONES
from services.case_service import case_rows
from services.portfolio_service import portfolio_metrics, related
from ui.components import header, kpis, table, case_picker


def render(repo, user, cases):
    header("Pricing & Market Access", "Decision, Governance & Strategy Platform")
    kpis(portfolio_metrics(cases))
    st.subheader("My Cases")
    table(case_rows([c for c in cases if c["owner"] == user]), ["Case ID", "Case", "Case Type", "Market", "Status", "Deadline"])
    case_picker(cases, "portfolio-case")
    st.subheader("Priority Actions")
    actions = [{"Case ID": c["id"], "Action": "Address reviewer feedback" if c["status"] == "Changes Requested" else "Complete evidence and submit" if c["status"] == "Draft" else "Review decision proposal", "Owner": c["owner"], "Due": c["deadline"]}
               for c in cases if c["status"] in {"Draft", "Changes Requested", "Under Review"}]
    table(actions)
    st.subheader("Upcoming Milestones")
    table(related(MILESTONES, cases))
    st.subheader("Recent Decisions / Alerts")
    ids = {c["id"] for c in cases}
    events = [e for e in repo.audit() if e["Case ID"] in ids]
    table(list(reversed(events[-5:])) if events else [
        {"Case ID": c["id"], "Status": c["status"], "Update": c["comments"][-1]["Comment"] if c["comments"] else "Demo decision recorded"}
        for c in cases if c["status"] in {"Approved", "Changes Requested"}])
