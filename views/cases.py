from datetime import date
import pandas as pd
import streamlit as st
from data.demo import PRODUCTS, MARKETS, MILESTONES
from domain.cases import CaseType, CASE_SCHEMAS, sections_for
from engine.pricing import price_outputs
from services.access_service import can_edit, can_review, can_view
from services.case_service import create_case, case_rows, save_inputs
from services.pricing_service import save_pricing
from services.approval_service import transition
from ui.components import header, case_header, navigation, navigate, table, note, case_picker


def render_list(repo, user, cases):
    header("Cases", "Manage pricing and access proposals from initial input to governed decision.")
    with st.container(horizontal=True):
        search = st.text_input("Search cases", placeholder="Case name, ID or product")
        kind = st.selectbox("Case type", ["All case types", *[str(k) for k in CaseType]])
        status = st.selectbox("Status", ["All statuses", "Draft", "Under Review", "Changes Requested", "Approved", "Rejected"])
    filtered = [c for c in cases if (kind == "All case types" or c["type"] == kind)
                and (status == "All statuses" or c["status"] == status)
                and search.casefold() in f'{c["id"]} {c["name"]} {c["product"]}'.casefold()]
    table(case_rows(filtered), ["Case ID", "Case", "Case Type", "Product", "Market", "Owner", "Status", "Deadline"])
    case_picker(filtered)
    if user in {"Maya Chen", "Ethan Brooks"}:
        st.button("New Case", type="primary", on_click=navigate, args=("Cases", "new"))
    else:
        st.caption("Select a case owner to create a new proposal.")


def render_new(repo, user):
    header("New Case", "Define the decision, product and accountable owner.", "Cases / New proposal")
    if user not in {"Maya Chen", "Ethan Brooks"}:
        note("Select Maya Chen or Ethan Brooks to create a case in this demo.")
        return
    with st.form("create-case"):
        name = st.text_input("Case name")
        case_type = st.selectbox("Case type", [str(k) for k in CaseType])
        product = st.selectbox("Product", PRODUCTS)
        market = st.selectbox("Market", MARKETS)
        deadline = st.date_input("Decision deadline", value=date(2026, 11, 30))
        st.caption(f"Owner · {user}")
        submitted = st.form_submit_button("Create draft", type="primary")
    if submitted:
        try:
            case_id = create_case(repo, user, name, case_type, product, market, deadline)
            navigate("Cases", case_id, "Overview")
            st.rerun()
        except (ValueError, PermissionError) as exc:
            st.error(str(exc))


def render_detail(repo, user, case_id):
    case = repo.get(case_id)
    if not case or not can_view(user, case):
        header("Case unavailable", "The case does not exist or is outside the selected demo user's visibility.")
        st.button("Back to Cases", on_click=navigate, args=("Cases",))
        return
    st.button("All Cases", type="tertiary", on_click=navigate, args=("Cases",))
    case_header(case)
    sections = sections_for(case["type"])
    selected = st.query_params.get("section", "Overview")
    selected = selected if selected in sections else "Overview"
    navigation(sections, selected, "case-nav", lambda s: navigate("Cases", case_id, s))
    editable = can_edit(user, case)
    if selected == "Overview":
        overview(repo, user, case, editable)
    elif selected == "Pricing":
        pricing(repo, user, case, editable)
    elif selected == "Forecast":
        forecast(repo, user, case, editable)
    elif selected == "Governance":
        governance(repo, user, case)
    elif selected == "Decision Case":
        decision_case(case)
    elif selected == "Financial Impact":
        st.subheader("Input → Bridge → Output")
        note("Financial impact awaits validated price, volume, cost and currency assumptions. No valuation has been calculated.")
        table([], ["Bridge item", "Currency", *[f"Y{i}" for i in range(1,11)]])
        with st.expander("Calculation detail"):
            st.write("Future engine: volume × net price → net revenue → costs → contribution. Zero-only rows will be omitted from output bridges when outputs are available.")
    elif selected == "Market & Competition":
        st.subheader("Evidence register")
        table([], ["Competitor", "Product", "Market position", "Price evidence", "Source", "As of"])
        note("Link validated competitor and reimbursement evidence before making a pricing recommendation.")
    elif selected == "Market Access":
        st.subheader("Access workstreams & readiness")
        table([m for m in MILESTONES if m["Case ID"] == case_id], ["Workstream", "Milestone", "Owner", "Due", "Status"])
        st.subheader("Action tracker")
        table([], ["Action", "Owner", "Due", "Status", "Dependency"])
    elif selected == "Contracting":
        st.subheader("Proposed agreement structure")
        table([], ["Counterparty", "Term", "Commitment", "Rebate mechanism", "Renewal", "Owner"])
        note("Capture obligations and approval dependencies here. Contract parsing is not connected.")


def overview(repo, user, case, editable):
    st.subheader("Decision objective")
    if case["status"] == "Changes Requested":
        note("Changes requested. Update the proposal and resubmit from Governance.")
    with st.form(f"overview-{case['id']}-{user}"):
        summary = st.text_area("Executive summary", value=case["summary"], disabled=not editable)
        details = {field: st.text_input(field, value=case["details"].get(field, ""), disabled=not editable)
                   for field in CASE_SCHEMAS[CaseType(case["type"])]["fields"]}
        save = st.form_submit_button("Save overview", disabled=not editable)
    if save:
        save_inputs(repo, case["id"], user, {"summary": summary, "details": details})
        st.success("Overview saved for this demo session.")
    st.subheader("Ownership & milestones")
    table([m for m in MILESTONES if m["Case ID"] == case["id"]], ["Workstream", "Milestone", "Owner", "Due", "Status"])
    if not editable:
        st.caption("Inputs are editable by the owner while the case is Draft or Changes Requested.")


def pricing(repo, user, case, editable):
    st.subheader("Commercial inputs")
    st.caption("Editable: list price and discount. SKU and currency are fixed reference fields. Save to refresh calculated outputs.")
    with st.form(f"pricing-{case['id']}-{user}"):
        edited = st.data_editor(pd.DataFrame(case["pricing"]), hide_index=True, width="stretch",
                                disabled=True if not editable else ["SKU", "Currency"],
                                column_config={"List price": st.column_config.NumberColumn(min_value=0, format="%.2f", required=True),
                                               "Discount %": st.column_config.NumberColumn(min_value=0, max_value=100, format="%.1f", required=True)})
        saved = st.form_submit_button("Save pricing inputs", disabled=not editable)
    if saved:
        try:
            save_pricing(repo, case["id"], user, edited.to_dict("records"))
            st.success("Pricing inputs saved.")
            case = repo.get(case["id"])
        except (ValueError, PermissionError) as exc:
            st.error(str(exc))
    st.subheader("Illustrative output")
    table(price_outputs(case["pricing"]))
    with st.expander("Calculation detail"):
        st.write("Illustrative net price = list price × (1 − discount / 100). Prices are per unit in the displayed currency. Tax, rebates, clawbacks and IRP effects are excluded from this simple demo arithmetic.")


def forecast(repo, user, case, editable):
    st.subheader("Multi-year assumptions")
    st.caption("Enter units for Y1–Y10. Blank cells mean no assumption has been supplied.")
    with st.form(f"forecast-{case['id']}-{user}"):
        edited = st.data_editor(pd.DataFrame(case["forecast"]), hide_index=True, width="stretch",
                                disabled=True if not editable else ["Measure"],
                                column_config={f"Y{i}": st.column_config.NumberColumn(min_value=0, width="small") for i in range(1,11)})
        save = st.form_submit_button("Save forecast inputs", disabled=not editable)
    if save:
        rows = edited.astype(object).where(edited.notna(), None).to_dict("records")
        save_inputs(repo, case["id"], user, {"forecast": rows})
        st.success("Forecast assumptions saved.")
    note("Forecast, market share and financial outputs will be provided by a dedicated service.")


def governance(repo, user, case):
    st.subheader("Decision workflow")
    table([{"Stage": "Owner submission", "Responsible": case["owner"], "Status": case["status"]},
           {"Stage": "Independent review", "Responsible": "Pricing / Finance / General Manager", "Status": "Pending" if case["status"] == "Under Review" else "See case status"}])
    note("Demo workflow: one independent review completes the decision. A return requires a comment and allows the owner to edit and resubmit.")
    actions = []
    if can_edit(user, case):
        actions = ["Submit" if case["status"] == "Draft" else "Resubmit"]
    elif can_review(user, case):
        actions = ["Approve", "Request Changes", "Reject"]
    if actions:
        with st.form(f"review-{case['id']}-{user}"):
            action = st.selectbox("Decision action", actions)
            comment = st.text_area("Reviewer / submission comment")
            submit = st.form_submit_button("Record decision", type="primary")
        if submit:
            try:
                transition(repo, case["id"], user, action, comment)
                st.rerun()
            except (PermissionError, ValueError) as exc:
                st.error(str(exc))
    st.subheader("Comments & reviewer feedback")
    table(case["comments"])
    st.subheader("Audit trail")
    table([e for e in repo.audit() if e["Case ID"] == case["id"]])


def decision_case(case):
    st.subheader("Executive summary")
    st.write(case["summary"] or "No executive summary supplied yet.")
    table([{"Decision requested": case["type"], "Product / market": f'{case["product"]} · {case["market"]}',
            "Accountable owner": case["owner"], "Deadline": case["deadline"], "Status": case["status"]}])
    for title, text in [("Strategic rationale", "Document the patient access objective and commercial rationale."),
                        ("Options & recommendation", "Compare the proposed position with realistic alternatives."),
                        ("Financial impact", "Pending validated assumptions and financial engine outputs."),
                        ("Risks & conditions", "Confirm evidence quality, reference pricing exposure and approval conditions."),
                        ("Implementation & ownership", "Confirm the accountable owner, decision deadline and workstream milestones.")]:
        st.subheader(title)
        st.caption(text)
    with st.expander("Supporting assumptions and calculation detail"):
        table(price_outputs(case["pricing"]))
        table(case["forecast"])
