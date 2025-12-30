"""
SCI Figure Toolkit
==================

Publication-ready figure quality control for scientific research.

Quick Start:
    >>> from sci_figure_toolkit import set_style, create_figure
    >>> set_style('nature')
    >>> fig, ax = create_figure(1, 1)

Features:
    - Journal-specific style presets
    - Automatic quality auditing
    - Design pattern implementations
    - Smart label placement
"""

__version__ = "1.0.0"
__author__ = "SCI Figure Toolkit Team"

from .standards import (
    JournalStandard,
    FigureSpec,
    get_standard,
    list_journals,
    register_standard,
)

from .style import (
    set_style,
    apply_style,
    create_figure,
    get_figure_size,
)

from .auditor import (
    FigureAuditor,
    CodeAuditor,
    Issue,
    IssueType,
    Severity,
)

from .patterns import (
    UnifiedLegend,
    InlineLabel,
    TitleAnnotation,
    smart_bar_labels,
    extend_ylim_for_labels,
)

from .utils import (
    save_figure,
    collect_legend_handles,
    remove_individual_legends,
    colorblind_palette,
    set_subplot_labels,
    inches_to_mm,
    mm_to_inches,
    cm_to_inches,
)

__all__ = [
    # Standards
    'JournalStandard',
    'FigureSpec',
    'get_standard',
    'list_journals',
    'register_standard',
    # Style
    'set_style',
    'apply_style',
    'create_figure',
    'get_figure_size',
    # Auditor
    'FigureAuditor',
    'CodeAuditor',
    'Issue',
    'IssueType',
    'Severity',
    # Patterns
    'UnifiedLegend',
    'InlineLabel',
    'TitleAnnotation',
    'smart_bar_labels',
    'extend_ylim_for_labels',
    # Utils
    'save_figure',
    'collect_legend_handles',
    'remove_individual_legends',
    'colorblind_palette',
    'set_subplot_labels',
    'inches_to_mm',
    'mm_to_inches',
    'cm_to_inches',
]
