"""Tests for journal standards module."""

import pytest
from sci_figure_toolkit.standards import (
    FigureSpec,
    JournalStandard,
    get_standard,
    list_journals,
    register_standard,
)


class TestFigureSpec:
    """Test FigureSpec dataclass."""

    def test_default_values(self):
        """Test default specification values."""
        spec = FigureSpec(name="test")
        assert spec.width_single == 3.5
        assert spec.width_double == 7.0
        assert spec.font_axis_label == 9
        assert spec.font_tick_label == 8
        assert spec.dpi == 600

    def test_custom_values(self):
        """Test custom specification values."""
        spec = FigureSpec(
            name="custom",
            width_single=3.0,
            width_double=6.0,
            font_axis_label=10,
            dpi=300,
        )
        assert spec.width_single == 3.0
        assert spec.width_double == 6.0
        assert spec.font_axis_label == 10
        assert spec.dpi == 300

    def test_immutable(self):
        """Test that FigureSpec is frozen (immutable)."""
        spec = FigureSpec(name="test")
        with pytest.raises(Exception):  # FrozenInstanceError
            spec.width_single = 4.0


class TestJournalStandard:
    """Test JournalStandard enum and registry."""

    def test_nature_standard(self):
        """Test Nature journal standard."""
        spec = get_standard(JournalStandard.NATURE)
        assert spec.name == "Nature"
        assert spec.width_single == 3.5
        assert spec.width_1_5col == 5.5
        assert spec.width_double == 7.0
        assert spec.font_axis_label == 7

    def test_science_standard(self):
        """Test Science journal standard."""
        spec = get_standard(JournalStandard.SCIENCE)
        assert spec.name == "Science"
        assert spec.width_single == 2.25

    def test_cell_standard(self):
        """Test Cell journal standard."""
        spec = get_standard(JournalStandard.CELL)
        assert spec.name == "Cell"

    def test_acs_standard(self):
        """Test ACS journal standard."""
        spec = get_standard(JournalStandard.ACS)
        assert spec.name == "ACS"
        assert spec.width_single == 3.25

    def test_get_standard_by_string(self):
        """Test getting standard by string name."""
        spec = get_standard("nature")
        assert spec.name == "Nature"

        spec = get_standard("SCIENCE")
        assert spec.name == "Science"

    def test_invalid_standard(self):
        """Test error on invalid standard name."""
        with pytest.raises((KeyError, ValueError)):
            get_standard("invalid_journal")


class TestListJournals:
    """Test list_journals function."""

    def test_returns_list(self):
        """Test that list_journals returns a list."""
        journals = list_journals()
        assert isinstance(journals, list)
        assert len(journals) > 0

    def test_contains_major_journals(self):
        """Test that major journals are in the list."""
        journals = list_journals()
        assert "nature" in journals or "NATURE" in journals.upper() if isinstance(journals[0], str) else True


class TestRegisterStandard:
    """Test custom standard registration."""

    def test_register_custom_standard(self):
        """Test registering a custom journal standard."""
        custom_spec = FigureSpec(
            name="CustomJournal",
            width_single=4.0,
            width_double=8.0,
            font_axis_label=11,
        )
        register_standard("custom", custom_spec)

        retrieved = get_standard("custom")
        assert retrieved.name == "CustomJournal"
        assert retrieved.width_single == 4.0
