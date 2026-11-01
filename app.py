"""Standalone Pricing & Market Access entry point. Does not import the legacy UI."""
import streamlit as st
from data.demo import SNAPSHOT
from data.repository import Repository
from services.case_service import visible_cases
from shared.legacy_helpers import PERSONAS
from ui.styles import inject_styles
from ui.components import navigation, navigate
from views import portfolio, catalog, cases as case_views

PAGES = ("Portfolio", "Prices", "Cases", "Market Access", "Tenders", "Contracts", "Intelligence", "Insights", "Admin")
# Retain the existing platform's shared personas relevant to this product.
DEMO_USERS = ("Maya Chen", "Ethan Brooks", "Priya Nair", "Daniel Ortiz", "Sarah Morgan", "Admin User")


def main():
    st.set_page_config(page_title="Pricing & Market Access", layout="wide", initial_sidebar_state="collapsed")
    inject_styles()
    st.markdown('<div class="brand">PRICING & MARKET ACCESS / DECISION WORKSPACE</div>', unsafe_allow_html=True)
    with st.expander("Demo identity & session"):
        user = st.selectbox("Acting as", DEMO_USERS, key="demo-user")
        st.caption(f"{PERSONAS[user]} · Demo role switching, not authentication. Changes are held in this session only.")
    repo = Repository(st.session_state)
    visible = visible_cases(repo, user)
    page = st.query_params.get("page", "Portfolio")
    page = page if page in PAGES else "Portfolio"
    navigation(PAGES, page, "primary-nav", navigate)
    if page == "Portfolio":
        portfolio.render(repo, user, visible)
    elif page == "Cases":
        case_id = st.query_params.get("case")
        if case_id == "new":
            case_views.render_new(repo, user)
        elif case_id:
            case_views.render_detail(repo, user, case_id)
        else:
            case_views.render_list(repo, user, visible)
    else:
        catalog.render(repo, user, visible, page)
    st.markdown(f'<div class="footer">Fictional demo data · Portfolio snapshot: {SNAPSHOT} · Session-only changes · Currency shown per record</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
