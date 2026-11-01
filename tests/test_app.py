"""Run with python -m unittest discover -s tests -v (no external services)."""
import hashlib
import json
from pathlib import Path
import unittest
from streamlit.testing.v1 import AppTest
from data.repository import Repository
from domain.cases import CaseType, sections_for
from services.case_service import create_case, save_inputs, visible_cases
from services.approval_service import transition
from services.pricing_service import save_pricing
from engine.pricing import price_outputs

ROOT = Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.repo = Repository({})

    def test_return_edit_resubmit_approve_and_audit(self):
        transition(self.repo, "PMA-001", "Priya Nair", "Request Changes", "Update evidence")
        save_inputs(self.repo, "PMA-001", "Maya Chen", {"summary": "Updated evidence"})
        transition(self.repo, "PMA-001", "Maya Chen", "Resubmit")
        transition(self.repo, "PMA-001", "Daniel Ortiz", "Approve", "Evidence confirmed")
        self.assertEqual(self.repo.get("PMA-001")["status"], "Approved")
        self.assertEqual(len(self.repo.audit()), 4)
        self.assertEqual(self.repo.get("PMA-001")["comments"][0]["Comment"], "Update evidence")
        with self.assertRaises(PermissionError):
            save_inputs(self.repo, "PMA-001", "Maya Chen", {"summary": "Locked"})

    def test_visibility_and_permission_guards(self):
        self.assertEqual(len(visible_cases(self.repo, "Maya Chen")), 4)
        self.assertEqual(len(visible_cases(self.repo, "Ethan Brooks")), 2)
        self.assertEqual(len(visible_cases(self.repo, "Admin User")), 6)
        with self.assertRaises(PermissionError):
            transition(self.repo, "PMA-001", "Maya Chen", "Approve")
        with self.assertRaises(PermissionError):
            save_inputs(self.repo, "PMA-002", "Maya Chen", {"summary": "Forbidden"})
        with self.assertRaises(ValueError):
            transition(self.repo, "PMA-001", "Priya Nair", "Request Changes", " ")
        self.assertEqual(self.repo.get("PMA-001")["status"], "Under Review")

    def test_creation_all_types_and_pricing_validation(self):
        for kind in CaseType:
            case_id = create_case(self.repo, "Maya Chen", "New proposal", kind, "Avenora 20 mg", "Germany", "2026-12-01")
            self.assertEqual(self.repo.get(case_id)["type"], str(kind))
            self.assertIn("Governance", sections_for(kind))
        self.assertEqual(price_outputs([{"List price": 120, "Discount %": 10}])[0]["Illustrative net price"], 108)
        with self.assertRaises(ValueError):
            save_pricing(self.repo, "PMA-005", "Maya Chen", [{"List price": 120, "Discount %": 101}])
        self.assertEqual(self.repo.get("PMA-005")["pricing"][0]["Discount %"], 10)

    def test_original_sources_unchanged(self):
        original = ROOT.parent / "ai-process-excellence"
        if not original.exists():
            self.skipTest("Original source project is not on this machine")
        manifest = json.loads((ROOT / "docs/source-manifest.json").read_text())
        for name, digest in manifest.items():
            self.assertEqual(hashlib.sha256((original / name).read_bytes()).hexdigest(), digest)


class RouteTests(unittest.TestCase):
    def app(self, page="Portfolio", case=None, section=None, user="Admin User"):
        app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
        app.session_state["demo-user"] = user
        app.query_params["page"] = page
        if case:
            app.query_params["case"] = case
        if section:
            app.query_params["section"] = section
        return app.run()

    def assert_clean(self, app):
        self.assertEqual(list(app.exception), [])

    def test_all_top_routes_and_subsections(self):
        from app import PAGES
        from views.catalog import SECTIONS
        for page in PAGES:
            for section in SECTIONS.get(page, (None,)):
                with self.subTest(page=page, section=section):
                    self.assert_clean(self.app(page, section=section))

    def test_all_case_types_and_sections(self):
        for i, kind in enumerate(CaseType, 1):
            for section in sections_for(kind):
                with self.subTest(case_type=kind, section=section):
                    self.assert_clean(self.app("Cases", f"PMA-{i:03}", section))

    def test_navigation_buttons_and_edit_persistence(self):
        app = self.app("Cases", "PMA-005", "Overview", "Maya Chen")
        app.text_area[0].set_value("A saved strategic rationale")
        next(b for b in app.button if b.label == "Save overview").click().run()
        self.assert_clean(app)
        next(b for b in app.button if b.label == "Pricing").click().run()
        self.assertEqual(app.query_params["section"], ["Pricing"])
        next(b for b in app.button if b.label == "Overview").click().run()
        self.assertEqual(app.text_area[0].value, "A saved strategic rationale")
        next(b for b in app.button if b.label == "Portfolio").click().run()
        self.assert_clean(app)
        self.assertNotIn("case", app.query_params)

    def test_new_case_submission_and_visibility(self):
        app = self.app("Cases", "new", user="Maya Chen")
        app.text_input[0].set_value("New access proposal")
        next(b for b in app.button if b.label == "Create draft").click().run()
        self.assert_clean(app)
        self.assertEqual(app.query_params["case"], ["PMA-007"])
        hidden = self.app("Cases", "PMA-002", user="Maya Chen")
        self.assertIn("Case unavailable", ''.join(m.value for m in hidden.markdown))
        restricted = self.app("Admin", user="Maya Chen")
        self.assertFalse(restricted.table)


if __name__ == "__main__":
    unittest.main()
