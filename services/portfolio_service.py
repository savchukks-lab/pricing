from data.demo import MILESTONES, TENDERS


def portfolio_metrics(cases):
    ids = {c["id"] for c in cases}
    active = [c for c in cases if c["status"] not in {"Approved", "Rejected"}]
    return [("Active Cases", str(len(active)), "Open decisions"),
            ("Pending Approvals", str(sum(c["status"] == "Under Review" for c in cases)), "Awaiting review"),
            ("Upcoming Tenders", str(sum(t["Case ID"] in ids for t in TENDERS)), "Demo pipeline"),
            ("Access Milestones", str(sum(m["Case ID"] in ids and m["Workstream"] == "Market Access" for m in MILESTONES)), "Next access checkpoint"),
            ("Revenue at Risk", f"€{sum(c['revenue_at_risk'] for c in active) / 1e6:.2f}m", "Illustrative EUR equivalent")]


def related(rows, cases):
    ids = {c["id"] for c in cases}
    return [row for row in rows if row["Case ID"] in ids]
