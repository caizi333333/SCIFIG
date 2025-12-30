"""
Journal Standards Library
=========================

Comprehensive collection of figure specifications for major scientific journals.

Usage:
    >>> from sci_figure_toolkit.standards import get_standard, FigureSpec
    >>> nature = get_standard('nature')
    >>> print(nature.width_single)  # 89mm = 3.5"
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple, List
from enum import Enum


class JournalCategory(Enum):
    """Journal category for grouping similar standards."""
    NATURE = "nature"
    SCIENCE = "science"
    CELL = "cell"
    ACS = "acs"
    RSC = "rsc"
    ELSEVIER = "elsevier"
    WILEY = "wiley"
    IEEE = "ieee"
    CUSTOM = "custom"


@dataclass(frozen=True)
class FigureSpec:
    """
    Figure specification for a journal.

    All measurements in inches unless otherwise noted.
    Font sizes in points (pt).

    Attributes:
        name: Journal display name
        category: Journal category for grouping

        # Dimensions (inches)
        width_single: Single column width
        width_1_5col: 1.5 column width
        width_double: Double/full column width
        max_height: Maximum figure height

        # Font sizes (pt)
        font_axis_label: Axis label font size
        font_tick_label: Tick label font size
        font_title: Title font size
        font_legend: Legend font size
        font_annotation: Annotation font size
        font_family: Font family name

        # Line properties
        line_width_data: Data line width
        line_width_fit: Fit/model line width
        line_width_reference: Reference line width
        line_width_axis: Axis spine width

        # Marker properties
        marker_size_data: Data marker size
        marker_size_highlight: Highlighted marker size

        # Output
        dpi: Output resolution (dots per inch)
        formats: Supported output formats

        # Colors
        color_cycle: Default color cycle

        # Notes
        notes: Additional journal-specific notes
    """

    # Identity
    name: str
    category: JournalCategory = JournalCategory.CUSTOM

    # Dimensions (inches)
    width_single: float = 3.5
    width_1_5col: float = 5.5
    width_double: float = 7.0
    max_height: float = 9.0

    # Font sizes (pt)
    font_axis_label: int = 9
    font_tick_label: int = 8
    font_title: int = 9
    font_legend: int = 8
    font_annotation: int = 7
    font_family: str = "sans-serif"

    # Line properties (pt)
    line_width_data: float = 1.5
    line_width_fit: float = 1.5
    line_width_reference: float = 1.0
    line_width_axis: float = 0.8

    # Marker properties (pt)
    marker_size_data: int = 4
    marker_size_highlight: int = 6

    # Output
    dpi: int = 600
    formats: Tuple[str, ...] = ("pdf", "png", "svg")

    # Colors (default matplotlib cycle)
    color_cycle: Tuple[str, ...] = (
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
        "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"
    )

    # Notes
    notes: str = ""

    @classmethod
    def from_journal(cls, journal: str) -> 'FigureSpec':
        """Create spec from journal name."""
        return get_standard(journal)

    def to_dict(self) -> Dict:
        """Convert to dictionary for matplotlib rcParams."""
        return {
            'figure.figsize': (self.width_double, self.width_double * 0.6),
            'figure.dpi': 100,
            'savefig.dpi': self.dpi,
            'font.size': self.font_axis_label,
            'font.family': self.font_family,
            'axes.labelsize': self.font_axis_label,
            'axes.titlesize': self.font_title,
            'axes.linewidth': self.line_width_axis,
            'xtick.labelsize': self.font_tick_label,
            'ytick.labelsize': self.font_tick_label,
            'legend.fontsize': self.font_legend,
            'lines.linewidth': self.line_width_data,
            'lines.markersize': self.marker_size_data,
            'axes.prop_cycle': f"cycler('color', {list(self.color_cycle)})",
        }

    def get_width(self, width_type: str) -> float:
        """Get width by type name."""
        width_map = {
            'single': self.width_single,
            '1.5col': self.width_1_5col,
            '1.5': self.width_1_5col,
            'double': self.width_double,
            'full': self.width_double,
        }
        return width_map.get(width_type.lower(), self.width_double)


# =============================================================================
# JOURNAL STANDARDS DATABASE
# =============================================================================

JOURNAL_STANDARDS: Dict[str, FigureSpec] = {}


def _register(spec: FigureSpec, *aliases: str) -> None:
    """Register a journal standard with optional aliases."""
    key = spec.name.lower().replace(' ', '_')
    JOURNAL_STANDARDS[key] = spec
    for alias in aliases:
        JOURNAL_STANDARDS[alias.lower()] = spec


# -----------------------------------------------------------------------------
# Nature Publishing Group
# -----------------------------------------------------------------------------

_register(
    FigureSpec(
        name="Nature",
        category=JournalCategory.NATURE,
        width_single=3.5,      # 89 mm
        width_1_5col=5.5,      # 140 mm
        width_double=7.0,      # 178 mm
        max_height=9.0,        # 229 mm
        font_axis_label=9,
        font_tick_label=8,
        font_title=9,
        font_legend=8,
        font_annotation=7,
        font_family="sans-serif",  # Arial/Helvetica preferred
        dpi=600,
        formats=("pdf", "eps", "tiff"),
        notes="Preferred fonts: Arial, Helvetica. Avoid serif fonts."
    ),
    "nature", "nat"
)

_register(
    FigureSpec(
        name="Nature Communications",
        category=JournalCategory.NATURE,
        width_single=3.5,
        width_1_5col=5.5,
        width_double=7.0,
        max_height=9.0,
        font_axis_label=9,
        font_tick_label=8,
        font_title=9,
        font_legend=8,
        font_annotation=7,
        font_family="sans-serif",
        dpi=600,
        notes="Same as Nature main journal."
    ),
    "nature_communications", "nat_comm", "ncomm"
)

# -----------------------------------------------------------------------------
# Science / AAAS
# -----------------------------------------------------------------------------

_register(
    FigureSpec(
        name="Science",
        category=JournalCategory.SCIENCE,
        width_single=2.25,     # 57 mm - narrower than Nature!
        width_1_5col=4.5,      # 114 mm
        width_double=6.0,      # 152 mm
        max_height=8.5,
        font_axis_label=8,     # Smaller than Nature
        font_tick_label=7,
        font_title=8,
        font_legend=7,
        font_annotation=6,
        font_family="sans-serif",  # Helvetica preferred
        dpi=600,
        formats=("pdf", "eps"),
        notes="Science uses narrower columns. Font sizes slightly smaller."
    ),
    "science", "sci"
)

_register(
    FigureSpec(
        name="Science Advances",
        category=JournalCategory.SCIENCE,
        width_single=3.5,      # More generous than Science
        width_1_5col=5.5,
        width_double=7.0,
        font_axis_label=9,
        font_tick_label=8,
        font_title=9,
        font_legend=8,
        font_annotation=7,
        font_family="sans-serif",
        dpi=600,
        notes="More flexible than Science main journal."
    ),
    "science_advances", "sci_adv"
)

# -----------------------------------------------------------------------------
# Cell Press
# -----------------------------------------------------------------------------

_register(
    FigureSpec(
        name="Cell",
        category=JournalCategory.CELL,
        width_single=3.35,     # 85 mm
        width_1_5col=5.0,      # 127 mm
        width_double=6.85,     # 174 mm
        max_height=9.0,
        font_axis_label=8,
        font_tick_label=7,
        font_title=8,
        font_legend=7,
        font_annotation=6,
        font_family="sans-serif",  # Arial preferred
        dpi=600,
        formats=("pdf", "eps", "tiff"),
        notes="Cell prefers compact figures. Arial font strongly preferred."
    ),
    "cell"
)

# -----------------------------------------------------------------------------
# ACS Publications
# -----------------------------------------------------------------------------

_register(
    FigureSpec(
        name="ACS (General)",
        category=JournalCategory.ACS,
        width_single=3.25,     # 82.5 mm
        width_1_5col=5.0,
        width_double=7.0,      # 178 mm
        max_height=9.5,
        font_axis_label=9,
        font_tick_label=8,
        font_title=10,
        font_legend=8,
        font_annotation=7,
        font_family="sans-serif",  # Arial, Helvetica
        dpi=600,
        formats=("pdf", "eps", "tiff"),
        color_cycle=(  # ACS recommended colors
            "#0072B2", "#D55E00", "#009E73", "#CC79A7",
            "#F0E442", "#56B4E9", "#E69F00", "#000000"
        ),
        notes="ACS recommends colorblind-safe palettes."
    ),
    "acs", "jacs", "acs_nano", "nano_letters"
)

# -----------------------------------------------------------------------------
# RSC Publications
# -----------------------------------------------------------------------------

_register(
    FigureSpec(
        name="RSC (General)",
        category=JournalCategory.RSC,
        width_single=3.25,     # 8.3 cm
        width_1_5col=5.0,
        width_double=6.75,     # 17.1 cm
        max_height=9.0,
        font_axis_label=9,
        font_tick_label=8,
        font_title=9,
        font_legend=8,
        font_annotation=7,
        font_family="sans-serif",
        dpi=600,
        formats=("pdf", "eps", "tiff"),
        notes="RSC journals follow similar standards."
    ),
    "rsc", "chem_comm", "chemical_communications"
)

# -----------------------------------------------------------------------------
# Elsevier
# -----------------------------------------------------------------------------

_register(
    FigureSpec(
        name="Elsevier (General)",
        category=JournalCategory.ELSEVIER,
        width_single=3.5,      # 90 mm
        width_1_5col=5.5,      # 140 mm
        width_double=7.0,      # 190 mm
        max_height=9.5,
        font_axis_label=9,
        font_tick_label=8,
        font_title=10,
        font_legend=8,
        font_annotation=7,
        font_family="sans-serif",  # Arial, Times, Courier
        dpi=600,
        formats=("pdf", "eps", "tiff", "jpg"),
        notes="Elsevier accepts wide range of formats. Check specific journal."
    ),
    "elsevier", "polymer"
)

# -----------------------------------------------------------------------------
# Wiley
# -----------------------------------------------------------------------------

_register(
    FigureSpec(
        name="Wiley (General)",
        category=JournalCategory.WILEY,
        width_single=3.25,     # 82 mm
        width_1_5col=5.0,      # 127 mm
        width_double=6.75,     # 171 mm
        max_height=9.0,
        font_axis_label=9,
        font_tick_label=8,
        font_title=9,
        font_legend=8,
        font_annotation=7,
        font_family="sans-serif",
        dpi=600,
        formats=("pdf", "eps", "tiff"),
        notes="Check specific Wiley journal for variations."
    ),
    "wiley", "angew", "adv_mater"
)

# -----------------------------------------------------------------------------
# IEEE
# -----------------------------------------------------------------------------

_register(
    FigureSpec(
        name="IEEE (General)",
        category=JournalCategory.IEEE,
        width_single=3.5,      # 3.5" standard
        width_1_5col=5.0,
        width_double=7.0,
        max_height=9.0,
        font_axis_label=10,    # IEEE prefers slightly larger
        font_tick_label=9,
        font_title=10,
        font_legend=9,
        font_annotation=8,
        font_family="serif",   # Times New Roman for IEEE
        dpi=600,
        formats=("pdf", "eps"),
        notes="IEEE traditionally uses serif fonts (Times)."
    ),
    "ieee"
)

# -----------------------------------------------------------------------------
# Default / Custom
# -----------------------------------------------------------------------------

DEFAULT_SPEC = FigureSpec(
    name="Default SCI",
    category=JournalCategory.CUSTOM,
    notes="Balanced defaults suitable for most SCI journals."
)

_register(DEFAULT_SPEC, "default", "sci", "standard")


# =============================================================================
# PUBLIC API
# =============================================================================

def get_standard(journal: str) -> FigureSpec:
    """
    Get figure specification for a journal.

    Args:
        journal: Journal name or alias (case-insensitive)

    Returns:
        FigureSpec for the journal

    Raises:
        KeyError: If journal not found

    Example:
        >>> spec = get_standard('nature')
        >>> print(spec.width_single)
        3.5
    """
    key = journal.lower().replace(' ', '_').replace('-', '_')
    if key not in JOURNAL_STANDARDS:
        available = ", ".join(sorted(set(
            s.name for s in JOURNAL_STANDARDS.values()
        )))
        raise KeyError(
            f"Unknown journal: '{journal}'. "
            f"Available: {available}"
        )
    return JOURNAL_STANDARDS[key]


def list_journals() -> List[str]:
    """
    List all available journal standards.

    Returns:
        Sorted list of journal names
    """
    return sorted(set(s.name for s in JOURNAL_STANDARDS.values()))


def register_standard(name: str, spec: FigureSpec) -> None:
    """
    Register a custom journal standard.

    Args:
        name: Key name for the standard (case-insensitive)
        spec: FigureSpec instance

    Example:
        >>> custom = FigureSpec(name="MyJournal", width_single=4.0)
        >>> register_standard("myjournal", custom)
    """
    JOURNAL_STANDARDS[name.lower()] = spec


def list_journals_by_category() -> Dict[str, List[str]]:
    """
    List journals grouped by category.

    Returns:
        Dictionary mapping category to journal names
    """
    result: Dict[str, List[str]] = {}
    for spec in set(JOURNAL_STANDARDS.values()):
        cat = spec.category.value
        if cat not in result:
            result[cat] = []
        result[cat].append(spec.name)

    # Sort each category
    for cat in result:
        result[cat] = sorted(result[cat])

    return result


# Backwards compatibility alias
JournalStandard = FigureSpec


# =============================================================================
# COMPARISON TABLE
# =============================================================================

def print_comparison_table() -> None:
    """Print comparison table of all journal standards."""

    print("\n" + "=" * 80)
    print("JOURNAL FIGURE STANDARDS COMPARISON")
    print("=" * 80)

    # Header
    print(f"\n{'Journal':<25} {'Single':<8} {'Double':<8} {'Font':<6} {'DPI':<6}")
    print("-" * 60)

    # Data rows
    seen = set()
    for spec in sorted(JOURNAL_STANDARDS.values(), key=lambda x: x.name):
        if spec.name in seen:
            continue
        seen.add(spec.name)

        print(f"{spec.name:<25} {spec.width_single:<8.2f} {spec.width_double:<8.2f} "
              f"{spec.font_axis_label:<6} {spec.dpi:<6}")

    print("\n" + "=" * 80)
    print("Dimensions in inches. Font size in points (pt).")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    print_comparison_table()
