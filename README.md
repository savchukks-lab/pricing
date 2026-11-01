# Pricing & Market Access

Standalone **Decision, Governance & Strategy Platform** skeleton built with Streamlit.
The adjacent AI Decision Platform is not imported or modified. No git commands are required.

## Start

Python 3.12+ is recommended; validated here on Python 3.14, Streamlit 1.58.0 and pandas 3.0.3.

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py --server.port 8502 --server.address 127.0.0.1
```

On this computer, `./run.ps1` also finds the installed Python runtime (or uses `.venv`).
Open http://127.0.0.1:8502. Portfolio is the landing view.

## Structure and file inventory

```text
app.py                         Entry point and validated query-parameter routing
run.ps1                        Windows launcher, separate port 8502
requirements.txt               Core dependencies
requirements-ai.txt            Optional AI SDK dependency
.streamlit/config.toml         Shared light theme, native sidebar navigation disabled
domain/cases.py                Six case types, applicable sections and type-specific fields
data/demo.py                   Fictional November 2026 portfolio and master records
data/repository.py             Isolated, session-scoped repository boundary
engine/pricing.py              Basic illustrative per-unit net-price arithmetic
services/access_service.py     Demo identity, visibility and action permissions
services/case_service.py       Case creation, filtered lists and guarded input updates
services/approval_service.py   Submit, return, resubmit, approve and reject
services/audit_service.py      Timestamped workflow/input events
services/portfolio_service.py  Portfolio counts, illustrative exposure, related records
services/pricing_service.py    Pricing validation and save boundary
services/ai_service.py         Lazy adapter to reused Responses service
shared/legacy_helpers.py       Verbatim extracted personas, money, pct and safe_float
shared/openai_service.py       Existing independent AI service, copied unchanged
ui/styles.py                  All application CSS and spacing/color/type tokens
ui/components.py              Headers, case header, text navigation, KPIs, tables, picker
views/portfolio.py             Landing portfolio
views/catalog.py               Seven other module skeletons and secondary navigation
views/cases.py                 Case list, creation and case sections
tests/test_app.py              Route, interaction, workflow and access regression checks
docs/reuse.md                  Source mapping, reuse choices and extension boundaries
docs/source-manifest.json      Original source checksums
docs/validation.md             Validation scope and results
```

Package folders also contain empty `__init__.py` markers. Generated caches and local test logs are not source artifacts.

## Navigation

Portfolio · Prices · Cases · Market Access · Tenders · Contracts · Intelligence · Insights · Admin.

Cases use Overview · Pricing · Market & Competition · Forecast · Market Access · Contracting · Financial Impact · Governance · Decision Case.
Contracting is currently hidden for Price Change and Launch Price. `CASE_SCHEMAS` controls applicability and the two initial fields for each type.
Prices, Intelligence and Admin have the requested secondary text navigation.
Query parameters support direct routes, for example `/?page=Cases&case=PMA-003&section=Governance`.
Button callbacks preserve the active session while updating the URL. Invalid routes fall back gracefully, and direct case URLs are permission checked.

## Demo walkthrough

1. Expand **Demo identity & session**. Maya Chen and Ethan Brooks own cases.
2. Open Cases, filter records, open a case or create a draft.
3. Owners can save the overview, pricing and Y1–Y10 volume assumptions while Draft or Changes Requested.
4. Submit from Governance. Switch to Priya Nair, Daniel Ortiz or Sarah Morgan for independent review.
5. Request Changes requires a comment. The owner can edit and resubmit; previous feedback stays visible.
6. An independent reviewer can approve or reject. Approved/rejected inputs are locked.
7. Select Admin User to inspect users, roles, reference lists, workflow definitions, integrations and audit.

## Scope

Fictional data is clearly labelled as a **1 November 2026 snapshot**. Revenue at Risk is a seeded illustrative EUR-equivalent amount, not a forecast or live currency conversion. Prices on the Prices page are case inputs, not an approved master-price registry.

Data and audit events last only for the current Streamlit session. Full browser reloads may start a new session. The identity selector demonstrates permission rules and is not authentication or production RBAC. The workflow intentionally uses a single independent review rather than the existing product's full multi-step approval matrix.

Forecast, IRP, tenders, contracts and financial modeling have clear UI/service extension points. No SAP, Salesforce, SSO, external price feeds, contract NLP, multi-tenancy or cost-effectiveness engine is connected. The optional AI service is reusable but is not automatically invoked; no case data is transmitted by the skeleton.

## Validation

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

For a constrained runner, point TEMP and TMP to a writable local folder before running Streamlit AppTest. See `docs/validation.md` for the tested flows and responsive checks.
