from html import escape
import streamlit as st


def header(title, subtitle="", eyebrow=""):
    if eyebrow:
        st.markdown(f'<div class="eyebrow">{escape(eyebrow)}</div>', unsafe_allow_html=True)
    st.markdown(f"<h1>{escape(title)}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="subtitle">{escape(subtitle)}</div>', unsafe_allow_html=True)


def note(text):
    st.markdown(f'<div class="notice">{escape(text)}</div>', unsafe_allow_html=True)


def case_header(case):
    header(case["name"], eyebrow=f'Cases / {case["type"]}')
    for fields in ((case["id"], case["market"], case["product"], case["status"]),
                   (f'Owner: {case["owner"]}', f'Last updated: {case["updated"]}', f'Decision deadline: {case["deadline"]}')):
        st.markdown(f'<div class="meta">{escape(" · ".join(fields))}</div>', unsafe_allow_html=True)


def kpis(items):
    cards = ''.join(f'<div class="kpi"><div class="kpi-label">{escape(label)}</div>'
                    f'<div class="kpi-value">{escape(value)}</div>'
                    f'<div class="kpi-context">{escape(context)}</div></div>' for label, value, context in items)
    st.markdown(f'<div class="kpi-grid">{cards}</div>', unsafe_allow_html=True)


def navigate(page, case_id=None, section=None):
    st.query_params.clear()
    st.query_params["page"] = page
    if case_id:
        st.query_params["case"] = case_id
    if section:
        st.query_params["section"] = section


def navigation(labels, current, key, callback):
    # Adapted from Investment Case's active text button + session rerun pattern.
    with st.container(key=key, horizontal=True, gap="small"):
        for label in labels:
            st.button(label, key=f"{key}-{label}", type="primary" if label == current else "tertiary",
                      on_click=callback, args=(label,))


def table(rows, columns=None, empty="No records in this demo view."):
    if not rows:
        st.caption(empty)
        if not columns:
            return
    columns = columns or list(rows[0])
    headings = ''.join(f'<th scope="col">{escape(str(c))}</th>' for c in columns)
    body = ''
    for row in rows:
        cells = ''
        for col in columns:
            value = row.get(col, "—")
            numeric = isinstance(value, (float, int))
            text = f"{value:,.2f}" if isinstance(value, float) else str(value)
            cells += f'<td class="{"number" if numeric else ""}">{escape(text)}</td>'
        body += f'<tr>{cells}</tr>'
    st.markdown(f'<div class="table-scroll" tabindex="0"><table class="pma-table"><thead><tr>{headings}</tr></thead><tbody>{body}</tbody></table></div>', unsafe_allow_html=True)


def case_picker(cases, key="open-case"):
    if not cases:
        return
    labels = {c["id"]: f'{c["id"]} · {c["name"]}' for c in cases}
    selected = st.selectbox("Select a case", list(labels), format_func=labels.get, key=key)
    st.button("Open case", key=f"{key}-button", type="tertiary", on_click=navigate, args=("Cases", selected, "Overview"))
