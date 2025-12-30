"""Tests for utility functions."""

import pytest
import os
import tempfile

pytest.importorskip("matplotlib")

import matplotlib.pyplot as plt
from sci_figure_toolkit.utils import (
    save_figure,
    collect_legend_handles,
    remove_individual_legends,
    set_subplot_labels,
    inches_to_mm,
    mm_to_inches,
    cm_to_inches,
    format_scientific,
    colorblind_palette,
)


class TestSaveFigure:
    """Test save_figure function."""

    @pytest.fixture
    def simple_figure(self):
        """Create a simple test figure."""
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 9])
        yield fig
        plt.close(fig)

    def test_save_single_format(self, simple_figure, tmp_path):
        """Test saving figure in single format."""
        filepath = str(tmp_path / "test_figure")
        saved = save_figure(simple_figure, filepath, formats=['png'], verbose=False)

        assert len(saved) == 1
        assert saved[0].endswith('.png')
        assert os.path.exists(saved[0])

    def test_save_multiple_formats(self, simple_figure, tmp_path):
        """Test saving figure in multiple formats."""
        filepath = str(tmp_path / "test_figure")
        saved = save_figure(
            simple_figure, filepath,
            formats=['pdf', 'png', 'svg'],
            verbose=False
        )

        assert len(saved) == 3
        for path in saved:
            assert os.path.exists(path)

    def test_save_with_dpi(self, simple_figure, tmp_path):
        """Test saving with custom DPI."""
        filepath = str(tmp_path / "test_figure")
        saved = save_figure(
            simple_figure, filepath,
            formats=['png'],
            dpi=300,
            verbose=False
        )

        assert os.path.exists(saved[0])

    def test_save_creates_directory(self, simple_figure, tmp_path):
        """Test that save_figure creates parent directories."""
        filepath = str(tmp_path / "subdir" / "nested" / "test_figure")
        saved = save_figure(simple_figure, filepath, formats=['png'], verbose=False)

        assert os.path.exists(saved[0])


class TestLegendHandling:
    """Test legend collection and removal functions."""

    @pytest.fixture
    def figure_with_legends(self):
        """Create a figure with multiple legends."""
        fig, axes = plt.subplots(1, 3)
        for i, ax in enumerate(axes):
            ax.plot([1, 2], [1, 2], label=f"Line {i}")
            ax.legend()
        yield fig, list(axes)
        plt.close(fig)

    def test_collect_handles(self, figure_with_legends):
        """Test collecting legend handles."""
        fig, axes = figure_with_legends
        handles, labels = collect_legend_handles(axes)

        assert len(handles) == 3
        assert len(labels) == 3
        assert "Line 0" in labels

    def test_collect_handles_deduplicate(self):
        """Test deduplication of legend handles."""
        fig, axes = plt.subplots(1, 2)
        for ax in axes:
            ax.plot([1, 2], [1, 2], label="Same Label")
        try:
            handles, labels = collect_legend_handles(list(axes), deduplicate=True)
            assert len(labels) == 1
            assert labels[0] == "Same Label"
        finally:
            plt.close(fig)

    def test_remove_legends(self, figure_with_legends):
        """Test removing individual legends."""
        fig, axes = figure_with_legends

        # All axes should have legends initially
        for ax in axes:
            assert ax.get_legend() is not None

        count = remove_individual_legends(axes)

        assert count == 3
        for ax in axes:
            assert ax.get_legend() is None


class TestSubplotLabels:
    """Test subplot labeling function."""

    @pytest.fixture
    def multi_panel_figure(self):
        """Create a multi-panel figure."""
        fig, axes = plt.subplots(1, 4)
        yield fig, list(axes)
        plt.close(fig)

    def test_default_labels(self, multi_panel_figure):
        """Test default (a), (b), (c), (d) labels."""
        fig, axes = multi_panel_figure
        set_subplot_labels(axes)

        # Check that text objects were added
        for i, ax in enumerate(axes):
            texts = ax.texts
            assert len(texts) >= 1
            expected_label = f"({chr(ord('a') + i)})"
            assert any(expected_label in t.get_text() for t in texts)

    def test_custom_format(self, multi_panel_figure):
        """Test custom label format."""
        fig, axes = multi_panel_figure
        set_subplot_labels(axes, fmt="{label})")

        for i, ax in enumerate(axes):
            texts = ax.texts
            expected = f"{chr(ord('a') + i)})"
            assert any(expected in t.get_text() for t in texts)

    def test_start_letter(self, multi_panel_figure):
        """Test starting from different letter."""
        fig, axes = multi_panel_figure
        set_subplot_labels(axes, start='e')

        texts = axes[0].texts
        assert any("(e)" in t.get_text() for t in texts)


class TestUnitConversion:
    """Test unit conversion functions."""

    def test_inches_to_mm(self):
        """Test inches to millimeters conversion."""
        assert inches_to_mm(1.0) == 25.4
        assert inches_to_mm(3.5) == pytest.approx(88.9, rel=0.01)

    def test_mm_to_inches(self):
        """Test millimeters to inches conversion."""
        assert mm_to_inches(25.4) == pytest.approx(1.0, rel=0.01)
        assert mm_to_inches(88.9) == pytest.approx(3.5, rel=0.01)

    def test_cm_to_inches(self):
        """Test centimeters to inches conversion."""
        assert cm_to_inches(2.54) == pytest.approx(1.0, rel=0.01)
        assert cm_to_inches(8.89) == pytest.approx(3.5, rel=0.01)

    def test_round_trip(self):
        """Test round-trip conversion."""
        original = 3.5
        converted = inches_to_mm(original)
        back = mm_to_inches(converted)
        assert back == pytest.approx(original, rel=0.001)


class TestFormatScientific:
    """Test scientific notation formatting."""

    def test_format_large_number(self):
        """Test formatting large numbers."""
        result = format_scientific(1.5e6)
        assert "1.5" in result
        assert "10" in result or "6" in result

    def test_format_small_number(self):
        """Test formatting small numbers."""
        result = format_scientific(3.2e-4)
        assert "3.2" in result

    def test_format_zero(self):
        """Test formatting zero."""
        result = format_scientific(0)
        assert result == "0"

    def test_format_regular_number(self):
        """Test formatting numbers near 1."""
        result = format_scientific(2.5, precision=2)
        assert "2.5" in result


class TestColorblindPalette:
    """Test colorblind-safe palette function."""

    def test_returns_colors(self):
        """Test that palette returns color list."""
        colors = colorblind_palette()
        assert isinstance(colors, list)
        assert len(colors) > 0

    def test_hex_format(self):
        """Test that colors are in hex format."""
        colors = colorblind_palette()
        for color in colors:
            assert color.startswith('#')
            assert len(color) == 7

    def test_custom_count(self):
        """Test requesting specific number of colors."""
        colors = colorblind_palette(n=3)
        assert len(colors) == 3

    def test_max_colors(self):
        """Test maximum color count."""
        colors = colorblind_palette(n=8)
        assert len(colors) == 8

    def test_exceeding_max(self):
        """Test requesting more colors than available."""
        colors = colorblind_palette(n=100)
        # Should return available colors, not fail
        assert len(colors) <= 100
