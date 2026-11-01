# Reuse and architecture

Source reviewed: `C:/Users/User/Documents/ai-process-excellence`.
No source files were modified. The three directly relevant source files are recorded by SHA-256 in `source-manifest.json`; the regression suite verifies them when the original project is available.

## Direct code reuse

- `shared/legacy_helpers.py`: `PERSONAS`, `money`, `pct` extracted verbatim from `streamlit_app.py`; `safe_float` extracted verbatim from `deal_logic.py`. The new identity/permission surface consumes the shared personas, and the illustrative pricing engine consumes `safe_float`. Formatting helpers remain available for future financial outputs.
- `shared/openai_service.py`: unchanged copy of the existing 110-line, UI-independent Responses service. `services/ai_service.py` provides a lazy boundary, so the optional SDK is unnecessary for normal startup. No automatic model calls occur.

The existing project is a large monolithic UI with module wrappers importing that UI. Importing it into this app would couple startup, styling, workflow state and data directories. Small helpers were extracted into this standalone project, with provenance, rather than copying or importing the large application. The original product can adopt these helpers later through a separately reviewed refactor.

## Reused patterns, adapted rather than claimed as direct code reuse

- **Investment Case:** active text-button navigation, case context header, executive Decision Case, compact KPIs, Y1–Y10 assumptions, calculation expanders and Input → Bridge → Output structure. Navigation now uses a wrapping horizontal container rather than nine fixed-width columns.
- **Deal Approval:** owner visibility, independent reviewer actions, locked approved inputs, Changes Requested → owner edit → resubmit, retained comments and before/after audit events. Full approval routing, delegation and existing financial models were deliberately not brought into this skeleton.
- **Launch Sandbox:** case-linked ownership, workstreams, due milestones, readiness/status and action-tracker structures. Milestones are seeded reference records; action and evidence registers are explicitly empty future surfaces.
- **Shared:** personas are reused directly; routing and UI composition patterns are adapted. CSS is newly centralized for this product's specified visual system, avoiding the original app's large global stylesheet.

## Boundaries

`views` → `services` → `engine` / `data.Repository`.
The domain contains case types/applicability and imports no UI framework.
Services enforce workflow and edit permissions independently of widget visibility.
The repository receives a mapping, currently Streamlit session state, and can be replaced by a durable backend.
The calculation engine is independent of Streamlit. Add forecast, IRP, tender and contract services only when their business behavior is specified; no empty service abstractions were added solely for future names.

## Shared visual system

All CSS lives in `ui/styles.py`, injected once at entry. `.streamlit/config.toml` supplies the matching native widget palette. `ui/components.py` is the single home for reusable headers, metadata, KPIs, text navigation and compact tables.
The tokens define Arial/Helvetica, white/neutral surfaces, a single teal accent, semantic risk colors, the requested 4–48px spacing scale and an 8px radius. Desktop content is capped at 1536px including 32px side padding. Mobile uses 16px side padding, one KPI per row, wrapped text navigation and scroll-contained tables. Shadows are suppressed globally; keyboard focus remains visible using outlines.
