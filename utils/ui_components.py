"""
Shared UI Components
======================
Reusable Streamlit UI elements — headers, page setup, sidebar, CSS.
"""

from __future__ import annotations

import streamlit as st


def setup_page(
    title: str,
    icon: str,
    show_back_button: bool = True,
) -> None:
    """Standard page configuration used by every sub-page."""
    st.set_page_config(
        page_title=f"{title} | GJMIP",
        page_icon=icon,
        layout="wide",
    )
    if show_back_button:
        with st.sidebar:
            if st.button("⬅️ Back to Home", use_container_width=True):
                st.switch_page("app.py")


def page_header(icon: str, title: str, subtitle: str) -> None:
    """Render a consistent page header."""
    st.markdown(
        f"""
        <div style="margin-bottom: 8px;">
            <span style="font-size: 2rem; font-weight: 800;
                         color: #E6EDF3;">{icon} {title}</span>
            <span style="color: #8B949E; font-size: 0.9rem;
                         margin-left: 12px;">{subtitle}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def gradient_divider() -> None:
    """Render a gradient horizontal rule."""
    st.markdown(
        '<div class="gradient-divider"></div>',
        unsafe_allow_html=True,
    )
