import html

import streamlit as st


def _responsible_disclosure():
    url = "www.fake-zero-copter.url"
    text = "Report a security issue"
    html = f'<a href="{url}">{text}</a>'
    return html


def footer(app_name: str):
    """
    Immediately draw the footer.
    :param app_name: Name to display in the footer
    """
    st.markdown("---")

    footer_parts = [html.escape(app_name), _responsible_disclosure()]

    footer = " — ".join(footer_parts)

    st.markdown(footer, unsafe_allow_html=True)

    return footer
