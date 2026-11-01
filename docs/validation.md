# Validation

Validated on 1 November 2026 with Python 3.14, Streamlit 1.58.0 and pandas 3.0.3.

## Automated

`python -m unittest discover -s tests -v` exercises eight tests:

- All nine top-level areas and every Prices, Intelligence and Admin subsection.
- All applicable sections across all six case types (52 case section combinations).
- Actual navigation button callbacks and overview save persistence across case sections.
- New-case form submission and redirection to the new case.
- Direct-link case visibility and restricted administration.
- Return with comment, owner update, resubmit and independent approval, including retained comments, audit events and locked final inputs.
- Owner/reviewer permission guards and invalid pricing rejection without mutation.
- Original source checksums against the reuse manifest.

The Streamlit server starts on its separate localhost port, 8502. Startup and browser rendering were checked. No git commands were used.

## Visual and responsive

Browser inspection covers the portfolio, text navigation and case screen at desktop and a 390 × 844 mobile viewport. Mobile KPIs stack in one column, navigation wraps, and tables remain within their own horizontal scroll regions.

Final DOM measurements:

- Desktop: viewport and document both 1280px; five KPI columns; page title 32px; section title 21px; table left border 0px; zero computed shadows across buttons, inputs and KPI cards.
- Mobile portfolio: viewport and document both 390px; one 348px KPI column; zero computed shadows.
- Mobile case: viewport and document both 390px; eight applicable text tabs; no form warnings after rendering.
- Final desktop/mobile captures: `desktop.jpg`, `mobile.jpg` in this folder. The viewport override was reset after testing.

All authored CSS is centralized in `ui/styles.py`; view files contain no style blocks. Native widget palette is centralized in `.streamlit/config.toml`.

## Limits

These are skeleton, session-state and simulated-role checks, not production security, persistence, accessibility certification, business model validation or integration testing. Multi-year forecast and financial outputs are intentionally uncalculated. Optional live AI calls and real third-party integrations were not tested or invoked.
