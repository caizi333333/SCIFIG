"""Tests for design patterns module."""

import pytest

pytest.importorskip("matplotlib")

import matplotlib.pyplot as plt
import numpy as np
from sci_figure_toolkit.patterns import (
    UnifiedLegend,
    TitleAnnotation,
    InlineLabel,
    smart_bar_labels,
)


class TestUnifiedLegend:
    """Test Pattern B: Unified bottom legend."""

    @pytest.fixture
    def multi_panel_figure(self):
        """Create a multi-panel figure with individual legends."""
        fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.5))
        for ax in axes:
            ax.plot([1, 2, 3], [1, 2, 3], 'b-', label="0.1 Hz")
            ax.plot([1, 2, 3], [2, 3, 4], 'r-', label="1.0 Hz")
            ax.legend()
        yield fig, list(axes)
        plt.close(fig)

    def test_apply_unified_legend(self, multi_panel_figure):
        """Test applying unified bottom legend."""
        fig, axes = multi_panel_figure

        legend = UnifiedLegend.apply(fig, axes)

        # Check that individual legends are removed
        for ax in axes:
            assert ax.get_legend() is None

        # Check that figure has a legend
        assert legend is not None

    def test_collect_handles(self, multi_panel_figure):
        """Test collecting legend handles from axes."""
        fig, axes = multi_panel_figure

        handles, labels = UnifiedLegend.collect_handles(axes)

        assert len(handles) > 0
        assert len(labels) > 0
        assert "0.1 Hz" in labels
        assert "1.0 Hz" in labels

    def test_deduplicate_labels(self, multi_panel_figure):
        """Test that duplicate labels are removed."""
        fig, axes = multi_panel_figure

        handles, labels = UnifiedLegend.collect_handles(axes, deduplicate=True)

        # Should only have 2 unique labels despite 3 subplots
        assert labels.count("0.1 Hz") == 1
        assert labels.count("1.0 Hz") == 1


class TestTitleAnnotation:
    """Test Pattern E: Title annotations."""

    def test_format_single_value(self):
        """Test formatting a single value in title."""
        title = TitleAnnotation.format(
            main_title="(a) L-curve Analysis",
            values={"Optimal λ": 1.4e-01}
        )
        assert "(a) L-curve Analysis" in title
        assert "λ" in title or "lambda" in title.lower() or "1.4" in title

    def test_format_multiple_values(self):
        """Test formatting multiple values in title."""
        title = TitleAnnotation.format(
            main_title="(b) Model Fit",
            values={"R²": 0.995, "RMSE": 0.023}
        )
        assert "(b) Model Fit" in title
        assert "0.995" in title or "R²" in title

    def test_format_with_note(self):
        """Test formatting with additional note."""
        title = TitleAnnotation.format(
            main_title="(c) E'' Comparison",
            note="Diagnostic only"
        )
        assert "(c) E'' Comparison" in title
        assert "Diagnostic" in title


class TestInlineLabel:
    """Test Pattern F: Inline labels for reference lines."""

    @pytest.fixture
    def figure_with_axes(self):
        """Create a simple figure with axes."""
        fig, ax = plt.subplots()
        ax.plot([0, 10], [0, 10])
        yield fig, ax
        plt.close(fig)

    def test_add_inline_label(self, figure_with_axes):
        """Test adding inline label to reference line."""
        fig, ax = figure_with_axes

        line = ax.axhline(5.0, color='red', linestyle='--')
        text = InlineLabel.add(ax, y=5.0, label=r'$\pm 3\sigma$')

        assert text is not None
        # Text should be positioned near y=5.0

    def test_inline_label_position(self, figure_with_axes):
        """Test inline label positioning options."""
        fig, ax = figure_with_axes

        # Right side (default)
        text_right = InlineLabel.add(ax, y=5.0, label="right", position='right')
        # Left side
        text_left = InlineLabel.add(ax, y=3.0, label="left", position='left')

        assert text_right is not None
        assert text_left is not None


class TestSmartBarLabels:
    """Test smart bar chart label placement."""

    @pytest.fixture
    def bar_chart(self):
        """Create a bar chart with positive and negative values."""
        fig, ax = plt.subplots()
        values = [0.8, 0.6, -0.1, 0.9, -0.2]
        bars = ax.bar(range(5), values)
        yield fig, ax, bars, values
        plt.close(fig)

    def test_smart_labels(self, bar_chart):
        """Test smart label placement for bars."""
        fig, ax, bars, values = bar_chart

        smart_bar_labels(ax, bars, values)

        # Check that texts were added
        texts = ax.texts
        assert len(texts) == len(values)

    def test_positive_label_above(self, bar_chart):
        """Test that positive bar labels are placed above."""
        fig, ax, bars, values = bar_chart

        smart_bar_labels(ax, bars, values)

        # Positive value labels should be above bars
        for text in ax.texts:
            text_str = text.get_text()
            if text_str.startswith("0.8") or text_str.startswith("0.6"):
                # These are positive values
                pos = text.get_position()
                # Label y position should be positive
                assert pos[1] >= 0

    def test_negative_label_below(self, bar_chart):
        """Test that negative bar labels are placed below."""
        fig, ax, bars, values = bar_chart

        smart_bar_labels(ax, bars, values)

        # Find texts with negative values
        for text in ax.texts:
            text_str = text.get_text()
            if "-0.1" in text_str or "-0.2" in text_str:
                # Check vertical alignment is 'top' (below the bar)
                assert text.get_va() == 'top'

    def test_label_format(self, bar_chart):
        """Test custom label format."""
        fig, ax, bars, values = bar_chart

        smart_bar_labels(ax, bars, values, fmt="{:.2f}")

        texts = [t.get_text() for t in ax.texts]
        assert "0.80" in texts
        assert "-0.10" in texts
