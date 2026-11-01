"""Session-scoped demo repository. Replace this boundary for durable storage."""
from copy import deepcopy
from data.demo import seed_cases


class Repository:
    def __init__(self, state):
        self.state = state
        if "pma_data" not in state:
            state["pma_data"] = {"cases": seed_cases(), "audit": []}

    def cases(self):
        return deepcopy(self.state["pma_data"]["cases"])

    def get(self, case_id):
        return next((c for c in self.cases() if c["id"] == case_id), None)

    def save(self, case):
        rows = self.state["pma_data"]["cases"]
        index = next((i for i, c in enumerate(rows) if c["id"] == case["id"]), None)
        if index is None:
            rows.append(deepcopy(case))
        else:
            rows[index] = deepcopy(case)

    def audit(self):
        return deepcopy(self.state["pma_data"]["audit"])

    def append_audit(self, event):
        self.state["pma_data"]["audit"].append(deepcopy(event))
