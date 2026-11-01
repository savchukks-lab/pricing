"""Small demo workflow adapting Deal Approval's return/resubmit concepts."""
from services.access_service import can_edit, can_review, can_view
from services.audit_service import record


def transition(repo, case_id, user, action, comment=""):
    case = repo.get(case_id)
    if not case or not can_view(user, case):
        raise PermissionError("This case is not available to the selected user.")
    before = case["status"]
    if action in {"Submit", "Resubmit"}:
        expected = "Draft" if action == "Submit" else "Changes Requested"
        if not can_edit(user, case) or before != expected:
            raise PermissionError("Only the owner may submit an editable case.")
        after = "Under Review"
    elif action in {"Approve", "Request Changes", "Reject"}:
        if not can_review(user, case):
            raise PermissionError("An independent reviewer must review this case.")
        if action in {"Request Changes", "Reject"} and not comment.strip():
            raise ValueError("Add a reviewer comment explaining the decision.")
        after = {"Approve": "Approved", "Request Changes": "Changes Requested", "Reject": "Rejected"}[action]
    else:
        raise ValueError("Unknown workflow action.")
    case["status"] = after
    if comment.strip():
        case["comments"].append({"Author": user, "Comment": comment.strip()})
    repo.save(case)
    record(repo, case_id, user, action, before, after, comment.strip())
    return after
