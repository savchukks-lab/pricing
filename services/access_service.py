"""Demo visibility and permission rules; no claim of authentication."""
from shared.legacy_helpers import PERSONAS

REVIEWERS = {"Priya Nair", "Daniel Ortiz", "Sarah Morgan"}


def can_view(user, case):
    return user in PERSONAS and (user in REVIEWERS or user == "Admin User" or case["owner"] == user)


def can_edit(user, case):
    return can_view(user, case) and user == case["owner"] and case["status"] in {"Draft", "Changes Requested"}


def can_review(user, case):
    return user in REVIEWERS and user != case["owner"] and case["status"] == "Under Review"


def can_admin(user):
    return user == "Admin User"
