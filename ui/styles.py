"""Single source for all application CSS and visual tokens."""
import streamlit as st

CSS = """
:root {
 --pma-bg:#FFFFFF; --pma-text:#1F2933; --pma-muted:#667085;
 --pma-border:#D9DEE5; --pma-subtle:#F7F8FA; --pma-accent:#176B68;
 --pma-positive:#235C43; --pma-warning:#89651E; --pma-risk:#8B3038;
 --space-1:4px; --space-2:8px; --space-3:12px; --space-4:16px;
 --space-5:20px; --space-6:24px; --space-8:32px; --space-10:40px; --space-12:48px;
 --pma-radius:8px; --pma-font:Arial,Helvetica,sans-serif;
}
html,body,[data-testid="stApp"],button,input,textarea,select,
[data-testid="stMarkdownContainer"], [data-baseweb] {font-family:var(--pma-font)!important;}
[data-testid="stAppViewContainer"] {background:var(--pma-bg);color:var(--pma-text);}
*, *::before, *::after {box-shadow:none!important;}
[data-testid="stMainBlockContainer"] {max-width:1536px;padding:32px;}
[data-testid="stMain"] {overflow-x:hidden;}
[data-testid="stHeader"] {display:none;}
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {display:none;}
h1 {font-size:32px!important;font-weight:700!important;line-height:1.15!important;letter-spacing:-.7px;padding:0!important;margin:8px 0 12px!important;}
h2 {font-size:21px!important;font-weight:600!important;line-height:1.3!important;margin:12px 0!important;padding:0!important;}
h3 {font-size:17px!important;font-weight:600!important;}
[data-testid="stHeading"] h3 {font-size:21px!important;font-weight:600!important;line-height:1.3!important;}
p, [data-testid="stMarkdownContainer"] p, label {font-size:14px;line-height:1.5;}
.subtitle {font-size:16px;color:var(--pma-muted);max-width:850px;margin-bottom:24px;}
.eyebrow {font-size:12.5px;color:var(--pma-accent);letter-spacing:.7px;text-transform:uppercase;}
.meta,.helper {font-size:13px;color:var(--pma-muted);line-height:1.4;}
.meta {margin-bottom:8px;}
.brand {font-size:13px;color:var(--pma-muted);letter-spacing:.35px;}
.kpi-grid {display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:16px;margin:8px 0 24px;}
.kpi {border:1px solid var(--pma-border);border-radius:var(--pma-radius);padding:20px;min-width:0;}
.kpi-label {font-size:13px;color:var(--pma-muted);}
.kpi-value {font-size:29px;font-weight:600;letter-spacing:-.7px;margin:8px 0;}
.kpi-context {font-size:12.5px;color:var(--pma-muted);}
button {border-radius:6px!important;font-size:14px!important;min-height:34px!important;}
button[kind="secondary"] {border:1px solid var(--pma-border)!important;background:white!important;color:var(--pma-text)!important;}
button[kind="primary"] {background:var(--pma-accent)!important;border:1px solid var(--pma-accent)!important;}
button[kind="tertiary"] {color:var(--pma-accent)!important;}
button:hover {border-color:var(--pma-accent)!important;}
button:focus-visible,a:focus-visible {outline:2px solid var(--pma-accent)!important;outline-offset:3px;}
.st-key-primary-nav,.st-key-case-nav,.st-key-section-nav {border-bottom:1px solid var(--pma-border);padding-bottom:8px;margin-bottom:20px;}
.st-key-primary-nav button,.st-key-case-nav button,.st-key-section-nav button {background:transparent!important;color:var(--pma-muted)!important;border:0!important;border-radius:0!important;padding:6px 10px!important;white-space:nowrap;}
.st-key-primary-nav button p {font-size:15px!important;font-weight:600;}
.st-key-case-nav button p,.st-key-section-nav button p {font-size:14px!important;}
.st-key-primary-nav button[kind="primary"],.st-key-case-nav button[kind="primary"],.st-key-section-nav button[kind="primary"] {color:var(--pma-accent)!important;border-bottom:2px solid var(--pma-accent)!important;}
[data-testid="stHorizontalBlock"] {min-width:0;}
[data-testid="stVerticalBlock"], [data-testid="stColumn"] {min-width:0;}
[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,[data-baseweb="select"]>div,textarea {border-radius:6px!important;font-size:14px!important;}
[data-baseweb="input"]:focus-within,[data-baseweb="textarea"]:focus-within,[data-baseweb="select"]:focus-within {border-color:var(--pma-accent)!important;}
[data-testid="stDataFrame"] {font-size:13px;max-width:100%;}
[data-testid="stExpander"] {border-color:var(--pma-border);border-radius:var(--pma-radius);}
.table-scroll {overflow-x:auto;max-width:100%;margin:8px 0;}
table.pma-table {width:100%;border-collapse:collapse;font-size:13px;text-align:left;}
.pma-table th {color:var(--pma-muted);font-weight:600;background:var(--pma-subtle);}
.pma-table td,.pma-table th {padding:12px;border:0;border-bottom:1px solid var(--pma-border);vertical-align:top;}
.pma-table .number {text-align:right;font-variant-numeric:tabular-nums;}
.status {color:var(--pma-accent);font-size:13px;}
.notice {border-left:2px solid var(--pma-accent);padding:8px 16px;margin:8px 0 16px;color:var(--pma-muted);font-size:13px;}
.footer {border-top:1px solid var(--pma-border);margin-top:32px;padding-top:16px;color:var(--pma-muted);font-size:12.5px;}
@media(max-width:1000px) {.kpi-grid {grid-template-columns:repeat(3,minmax(0,1fr));}}
@media(max-width:640px) {
 [data-testid="stMainBlockContainer"] {padding:24px 16px;}
 h1 {font-size:28px!important;overflow-wrap:anywhere;}
 .kpi-grid {grid-template-columns:1fr;gap:12px;}
 .kpi {padding:20px;}
 .st-key-primary-nav,.st-key-case-nav,.st-key-section-nav {max-width:100%;}
 [data-testid="stHorizontalBlock"] {flex-wrap:wrap!important;}
 [data-testid="stColumn"] {width:100%!important;flex:1 1 100%!important;}
}
"""


def inject_styles():
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)
