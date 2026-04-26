"""
Chart Helpers
===============
Shared Plotly layout defaults and chart-building utilities.
Eliminates duplicated styling across every page.
"""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go

# ── Base Layout ──────────────────────────────────────────────────────

_BASE_LAYOUT: dict[str, Any] = {
    "template": "plotly_dark",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"family": "Inter, -apple-system, sans-serif", "color": "#E6EDF3"},
    "margin": {"l": 0, "r": 20, "t": 10, "b": 0},
}

_GRID_COLOR = "rgba(102,126,234,0.06)"


def apply_default_layout(
    fig: go.Figure,
    *,
    height: int = 400,
    show_legend: bool = True,
    legend_horizontal: bool = False,
    coloraxis_showscale: bool = True,
    title: str | None = None,
) -> go.Figure:
    """Apply the standard dark-theme layout to any Plotly figure."""
    layout_kwargs: dict[str, Any] = {
        **_BASE_LAYOUT,
        "height": height,
        "showlegend": show_legend,
        "coloraxis_showscale": coloraxis_showscale,
    }

    if title:
        layout_kwargs["title"] = {"text": title, "font": {"size": 14}}

    if legend_horizontal:
        layout_kwargs["legend"] = {
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "title": "",
        }

    fig.update_layout(**layout_kwargs)

    fig.update_xaxes(gridcolor=_GRID_COLOR)
    fig.update_yaxes(gridcolor=_GRID_COLOR)

    return fig


def format_currency(value: float, decimals: int = 0) -> str:
    """Format a number as USD currency string."""
    if decimals == 0:
        return f"${value:,.0f}"
    return f"${value:,.{decimals}f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format a number as a percentage string."""
    return f"{value:.{decimals}f}%"


# ── Gradient color scales used across the app ────────────────────────
GRADIENT_PURPLE = ["#1a1f2e", "#667EEA", "#764BA2"]
GRADIENT_GREEN = ["#1a1f2e", "#48BB78", "#38B2AC"]
GRADIENT_WARM = ["#1a1f2e", "#D69E2E", "#ED8936"]
GRADIENT_DIVERGING = ["#E53E3E", "#0E1117", "#48BB78"]
HEATMAP_SCALE = ["#0E1117", "#667EEA", "#764BA2"]
