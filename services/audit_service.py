from datetime import datetime, timezone


def record(repo, case_id, user, action, before="", after="", comment=""):
    repo.append_audit({"Timestamp (UTC)": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                       "Case ID": case_id, "Actor": user, "Action": action,
                       "Previous status": before, "New status": after, "Comment": comment})
