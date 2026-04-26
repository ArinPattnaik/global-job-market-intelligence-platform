"""
Tests for Chart Helper Utilities
"""

import plotly.graph_objects as go
import pytest

from utils.chart_helpers import (
    apply_default_layout,
    format_currency,
    format_percentage,
)


class TestFormatCurrency:
    def test_basic(self):
        assert format_currency(50000) == "$50,000"

    def test_with_decimals(self):
        assert format_currency(50000.5, decimals=2) == "$50,000.50"

    def test_large_number(self):
        assert format_currency(1_234_567) == "$1,234,567"

    def test_zero(self):
        assert format_currency(0) == "$0"


class TestFormatPercentage:
    def test_basic(self):
        assert format_percentage(75.5) == "75.5%"

    def test_zero_decimals(self):
        assert format_percentage(75.5, decimals=0) == "76%"


class TestApplyDefaultLayout:
    def test_applies_dark_theme(self):
        fig = go.Figure()
        result = apply_default_layout(fig, height=300)
        layout = result.layout
        assert layout.template.layout.to_plotly_json() is not None
        assert layout.height == 300

    def test_returns_same_figure(self):
        fig = go.Figure()
        result = apply_default_layout(fig)
        assert result is fig
