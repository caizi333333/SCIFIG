"""
Figure Quality Auditor
======================

Automated detection of common figure quality issues.

Usage:
    >>> from sci_figure_toolkit import FigureAuditor
    >>> auditor = FigureAuditor(journal='nature')
    >>> issues = auditor.audit_figure(fig, axes)
    >>> auditor.report()
"""

import re
import ast
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple, Set
from enum import Enum, auto
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .standards import get_standard, FigureSpec, DEFAULT_SPEC


class Severity(Enum):
    """Issue severity levels."""
    ERROR = auto()      # Must fix before submission
    WARNING = auto()    # Should fix
    INFO = auto()       # Suggestion for improvement


class IssueType(Enum):
    """Types of figure quality issues."""

    # Legend issues
    REDUNDANT_LEGEND = "redundant_legend"
    LEGEND_OCCLUSION = "legend_occlusion"
    LEGEND_MISMATCH = "legend_mismatch"

    # Annotation issues
    ANNOTATION_OCCLUSION = "annotation_occlusion"
    BROKEN_ANNOTATION = "broken_annotation"

    # Size/format issues
    NON_STANDARD_SIZE = "non_standard_size"
    LOW_DPI = "low_dpi"

    # Font issues
    INCONSISTENT_FONTS = "inconsistent_fonts"
    FONT_TOO_SMALL = "font_too_small"
    FONT_TOO_LARGE = "font_too_large"

    # Bar chart issues
    BAR_LABEL_CUTOFF = "bar_label_cutoff"
    BAR_LABEL_OVERLAP = "bar_label_overlap"

    # Style issues
    MISSING_LABELS = "missing_labels"
    INCONSISTENT_COLORS = "inconsistent_colors"

    # Code issues (for CodeAuditor)
    HARDCODED_SIZE = "hardcoded_size"
    HARDCODED_FONT = "hardcoded_font"
    MISSING_TIGHT_LAYOUT = "missing_tight_layout"
    INEFFICIENT_LEGEND = "inefficient_legend"


@dataclass
class Issue:
    """Represents a single quality issue."""

    type: IssueType
    severity: Severity
    message: str
    suggestion: str
    location: Optional[str] = None  # subplot index or line number
    auto_fixable: bool = False
    fix_code: Optional[str] = None

    def __str__(self) -> str:
        icon = {
            Severity.ERROR: "❌",
            Severity.WARNING: "⚠️",
            Severity.INFO: "ℹ️"
        }[self.severity]

        loc = f" [{self.location}]" if self.location else ""
        fix = " (auto-fixable)" if self.auto_fixable else ""

        return (
            f"{icon} [{self.severity.name}] {self.type.value}{loc}{fix}\n"
            f"   {self.message}\n"
            f"   → {self.suggestion}"
        )


class FigureAuditor:
    """
    Audit matplotlib figures for quality issues.

    Example:
        >>> fig, axes = plt.subplots(1, 3)
        >>> # ... plotting ...
        >>> auditor = FigureAuditor(journal='nature')
        >>> issues = auditor.audit_figure(fig, axes)
        >>> auditor.report()
    """

    def __init__(
        self,
        journal: str = 'default',
        strict: bool = False
    ):
        """
        Initialize auditor.

        Args:
            journal: Journal name for standards reference
            strict: If True, treat warnings as errors
        """
        self.spec = get_standard(journal)
        self.strict = strict
        self.issues: List[Issue] = []

    def audit_figure(
        self,
        fig: plt.Figure,
        axes: Optional[Any] = None
    ) -> List[Issue]:
        """
        Audit a matplotlib figure.

        Args:
            fig: matplotlib Figure object
            axes: Axes or array of Axes (optional, will extract from fig)

        Returns:
            List of Issue objects
        """
        self.issues = []

        # Get axes if not provided
        if axes is None:
            axes = fig.get_axes()
        elif hasattr(axes, 'flat'):
            axes = list(axes.flat)
        elif not isinstance(axes, list):
            axes = [axes]

        # Run all checks
        self._check_figure_size(fig)
        self._check_redundant_legends(axes)
        self._check_font_consistency(axes)
        self._check_legend_occlusion(axes)
        self._check_missing_labels(axes)

        return self.issues

    def _check_figure_size(self, fig: plt.Figure) -> None:
        """Check if figure size matches journal standards."""
        width, height = fig.get_size_inches()

        valid_widths = [
            self.spec.width_single,
            self.spec.width_1_5col,
            self.spec.width_double
        ]

        # Check width
        if not any(abs(width - w) < 0.1 for w in valid_widths):
            self.issues.append(Issue(
                type=IssueType.NON_STANDARD_SIZE,
                severity=Severity.INFO,
                message=f"Figure width {width:.2f}\" doesn't match {self.spec.name} standards",
                suggestion=f"Use one of: {valid_widths} inches",
                auto_fixable=True,
                fix_code=f"fig.set_size_inches({self.spec.width_double}, {height:.2f})"
            ))

        # Check max height
        if height > self.spec.max_height:
            self.issues.append(Issue(
                type=IssueType.NON_STANDARD_SIZE,
                severity=Severity.WARNING,
                message=f"Figure height {height:.2f}\" exceeds max {self.spec.max_height}\"",
                suggestion=f"Reduce height to ≤ {self.spec.max_height}\"",
                auto_fixable=True,
                fix_code=f"fig.set_size_inches({width:.2f}, {self.spec.max_height})"
            ))

    def _check_redundant_legends(self, axes: List[plt.Axes]) -> None:
        """Check for redundant legends across subplots."""
        legends_content: Dict[int, Set[str]] = {}

        for i, ax in enumerate(axes):
            legend = ax.get_legend()
            if legend is not None:
                texts = frozenset(t.get_text() for t in legend.get_texts())
                if texts:
                    legends_content[i] = texts

        # Find overlapping legends
        if len(legends_content) > 1:
            items = list(legends_content.items())
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    idx1, texts1 = items[i]
                    idx2, texts2 = items[j]
                    overlap = texts1 & texts2

                    if overlap:
                        self.issues.append(Issue(
                            type=IssueType.REDUNDANT_LEGEND,
                            severity=Severity.WARNING,
                            message=(
                                f"Subplots {idx1} and {idx2} share legend items: "
                                f"{sorted(overlap)}"
                            ),
                            suggestion="Use Pattern B: unified bottom legend with fig.legend()",
                            location=f"subplots {idx1}, {idx2}",
                            auto_fixable=True,
                            fix_code=(
                                "# Remove individual legends\n"
                                "for ax in axes:\n"
                                "    if ax.get_legend():\n"
                                "        ax.get_legend().remove()\n\n"
                                "# Add unified legend\n"
                                "handles, labels = axes[0].get_legend_handles_labels()\n"
                                "fig.legend(handles, labels, loc='lower center',\n"
                                "           bbox_to_anchor=(0.5, -0.02), ncol=len(labels))"
                            )
                        ))
                        return  # Only report once

    def _check_font_consistency(self, axes: List[plt.Axes]) -> None:
        """Check for inconsistent font sizes."""
        title_sizes: Set[float] = set()
        label_sizes: Set[float] = set()

        for ax in axes:
            if ax.title.get_text():
                title_sizes.add(ax.title.get_fontsize())

            if ax.xaxis.label.get_text():
                label_sizes.add(ax.xaxis.label.get_fontsize())
            if ax.yaxis.label.get_text():
                label_sizes.add(ax.yaxis.label.get_fontsize())

        # Check title consistency
        if len(title_sizes) > 1:
            self.issues.append(Issue(
                type=IssueType.INCONSISTENT_FONTS,
                severity=Severity.WARNING,
                message=f"Inconsistent title font sizes: {sorted(title_sizes)}",
                suggestion=f"Use consistent size: {self.spec.font_title} pt",
                auto_fixable=True,
                fix_code=f"for ax in axes: ax.title.set_fontsize({self.spec.font_title})"
            ))

        # Check label consistency
        if len(label_sizes) > 1:
            self.issues.append(Issue(
                type=IssueType.INCONSISTENT_FONTS,
                severity=Severity.WARNING,
                message=f"Inconsistent label font sizes: {sorted(label_sizes)}",
                suggestion=f"Use consistent size: {self.spec.font_axis_label} pt",
                auto_fixable=True,
                fix_code=(
                    f"for ax in axes:\n"
                    f"    ax.xaxis.label.set_fontsize({self.spec.font_axis_label})\n"
                    f"    ax.yaxis.label.set_fontsize({self.spec.font_axis_label})"
                )
            ))

        # Check if fonts are within acceptable range
        all_sizes = title_sizes | label_sizes
        for size in all_sizes:
            if size < 6:
                self.issues.append(Issue(
                    type=IssueType.FONT_TOO_SMALL,
                    severity=Severity.ERROR,
                    message=f"Font size {size} pt is too small for print",
                    suggestion="Minimum readable font size is 6-7 pt",
                    auto_fixable=False
                ))
            elif size > 14:
                self.issues.append(Issue(
                    type=IssueType.FONT_TOO_LARGE,
                    severity=Severity.INFO,
                    message=f"Font size {size} pt may be too large",
                    suggestion="Consider reducing to 9-10 pt",
                    auto_fixable=False
                ))

    def _check_legend_occlusion(self, axes: List[plt.Axes]) -> None:
        """Check for potential legend-data occlusion."""
        for i, ax in enumerate(axes):
            legend = ax.get_legend()
            if legend is None:
                continue

            # Get legend location code
            loc = legend._loc
            loc_name = {
                1: "upper right", 2: "upper left",
                3: "lower left", 4: "lower right",
                9: "upper center", 10: "upper right"
            }.get(loc, "unknown")

            # Upper positions are more likely to occlude
            if loc in [1, 2, 9, 10]:
                self.issues.append(Issue(
                    type=IssueType.LEGEND_OCCLUSION,
                    severity=Severity.INFO,
                    message=f"Subplot {i}: legend in {loc_name} may occlude data",
                    suggestion="Verify visually. Consider Pattern B (unified bottom) or Pattern E (title)",
                    location=f"subplot {i}",
                    auto_fixable=False
                ))

    def _check_missing_labels(self, axes: List[plt.Axes]) -> None:
        """Check for missing axis labels."""
        for i, ax in enumerate(axes):
            if not ax.xaxis.label.get_text():
                self.issues.append(Issue(
                    type=IssueType.MISSING_LABELS,
                    severity=Severity.WARNING,
                    message=f"Subplot {i}: missing x-axis label",
                    suggestion="Add descriptive x-axis label with units",
                    location=f"subplot {i}",
                    auto_fixable=False
                ))

            if not ax.yaxis.label.get_text():
                self.issues.append(Issue(
                    type=IssueType.MISSING_LABELS,
                    severity=Severity.WARNING,
                    message=f"Subplot {i}: missing y-axis label",
                    suggestion="Add descriptive y-axis label with units",
                    location=f"subplot {i}",
                    auto_fixable=False
                ))

    def report(self, verbose: bool = True) -> str:
        """
        Generate audit report.

        Args:
            verbose: If True, print to stdout

        Returns:
            Report string
        """
        if not self.issues:
            msg = f"✅ Figure passed all {self.spec.name} checks!"
            if verbose:
                print(msg)
            return msg

        # Group by severity
        errors = [i for i in self.issues if i.severity == Severity.ERROR]
        warnings = [i for i in self.issues if i.severity == Severity.WARNING]
        infos = [i for i in self.issues if i.severity == Severity.INFO]

        lines = [
            "",
            "=" * 70,
            f"FIGURE AUDIT REPORT ({self.spec.name} Standards)",
            "=" * 70,
            "",
            f"Found {len(self.issues)} issues: "
            f"{len(errors)} errors, {len(warnings)} warnings, {len(infos)} info",
            "",
        ]

        # List issues by severity
        for issue in errors + warnings + infos:
            lines.append(str(issue))
            lines.append("")

        lines.append("=" * 70)

        report = "\n".join(lines)
        if verbose:
            print(report)

        return report

    def get_fix_suggestions(self) -> List[str]:
        """Get auto-fix code suggestions."""
        return [
            issue.fix_code
            for issue in self.issues
            if issue.auto_fixable and issue.fix_code
        ]


class CodeAuditor:
    """
    Audit Python plotting code for best practices.

    Example:
        >>> auditor = CodeAuditor(journal='nature')
        >>> issues = auditor.audit_file('figure_generation.py')
        >>> auditor.report()
    """

    # Patterns to detect
    PATTERNS = {
        # Hardcoded sizes
        r'figsize\s*=\s*\(\s*(\d+\.?\d*)\s*,': 'hardcoded_figsize',
        r'fontsize\s*=\s*(\d+)': 'hardcoded_fontsize',
        r'\.set_size_inches\s*\(\s*(\d+\.?\d*)': 'hardcoded_size',

        # Missing best practices
        r'ax\.legend\s*\(': 'individual_legend',
        r'plt\.savefig.*dpi\s*=\s*(\d+)': 'dpi_setting',

        # Potential issues
        r'\.text\s*\([^)]*transform\s*=\s*ax\.transAxes': 'text_annotation',
        r'bbox\s*=\s*dict': 'text_box',
    }

    def __init__(self, journal: str = 'default'):
        """Initialize code auditor."""
        self.spec = get_standard(journal)
        self.issues: List[Issue] = []

    def audit_file(self, filepath: str) -> List[Issue]:
        """
        Audit a Python file.

        Args:
            filepath: Path to Python file

        Returns:
            List of issues
        """
        self.issues = []

        with open(filepath, 'r') as f:
            content = f.read()
            lines = content.split('\n')

        self._check_patterns(lines)
        self._check_imports(content)
        self._check_style_consistency(content)

        return self.issues

    def audit_code(self, code: str) -> List[Issue]:
        """
        Audit Python code string.

        Args:
            code: Python code as string

        Returns:
            List of issues
        """
        self.issues = []
        lines = code.split('\n')

        self._check_patterns(lines)
        self._check_imports(code)
        self._check_style_consistency(code)

        return self.issues

    def _check_patterns(self, lines: List[str]) -> None:
        """Check for problematic patterns."""
        legend_calls = []

        for i, line in enumerate(lines, 1):
            # Check for individual legend calls (potential Pattern B violation)
            if re.search(r'ax\d*\.legend\s*\(', line) or re.search(r'axes?\[?\d*\]?\.legend\s*\(', line):
                legend_calls.append(i)

            # Check hardcoded figsize
            match = re.search(r'figsize\s*=\s*\(\s*(\d+\.?\d*)\s*,\s*(\d+\.?\d*)\s*\)', line)
            if match:
                width = float(match.group(1))
                valid_widths = [self.spec.width_single, self.spec.width_1_5col, self.spec.width_double]
                if not any(abs(width - w) < 0.1 for w in valid_widths):
                    self.issues.append(Issue(
                        type=IssueType.HARDCODED_SIZE,
                        severity=Severity.INFO,
                        message=f"Line {i}: figsize width {width}\" may not match journal standards",
                        suggestion=f"Use standard widths: {valid_widths}",
                        location=f"line {i}",
                        auto_fixable=True
                    ))

            # Check DPI setting
            match = re.search(r'dpi\s*=\s*(\d+)', line)
            if match:
                dpi = int(match.group(1))
                if dpi < 300:
                    self.issues.append(Issue(
                        type=IssueType.LOW_DPI,
                        severity=Severity.WARNING,
                        message=f"Line {i}: DPI {dpi} is too low for publication",
                        suggestion=f"Use dpi={self.spec.dpi} for publication quality",
                        location=f"line {i}",
                        auto_fixable=True
                    ))

        # Check for multiple legend calls (Pattern B suggestion)
        if len(legend_calls) > 1:
            self.issues.append(Issue(
                type=IssueType.INEFFICIENT_LEGEND,
                severity=Severity.INFO,
                message=f"Multiple ax.legend() calls at lines: {legend_calls}",
                suggestion="Consider Pattern B: unified bottom legend with fig.legend()",
                auto_fixable=False
            ))

    def _check_imports(self, content: str) -> None:
        """Check for recommended imports."""
        if 'sci_figure_toolkit' not in content:
            self.issues.append(Issue(
                type=IssueType.MISSING_LABELS,  # Reusing type
                severity=Severity.INFO,
                message="sci_figure_toolkit not imported",
                suggestion="from sci_figure_toolkit import set_style; set_style('nature')",
                auto_fixable=True
            ))

    def _check_style_consistency(self, content: str) -> None:
        """Check for style consistency."""
        # Check if tight_layout is called
        if 'plt.savefig' in content or 'fig.savefig' in content:
            if 'tight_layout' not in content and 'constrained_layout' not in content:
                self.issues.append(Issue(
                    type=IssueType.MISSING_TIGHT_LAYOUT,
                    severity=Severity.WARNING,
                    message="No tight_layout() call before savefig()",
                    suggestion="Add plt.tight_layout() or use constrained_layout=True",
                    auto_fixable=True,
                    fix_code="plt.tight_layout()"
                ))

    def report(self, verbose: bool = True) -> str:
        """Generate audit report."""
        if not self.issues:
            msg = "✅ Code follows best practices!"
            if verbose:
                print(msg)
            return msg

        lines = [
            "",
            "=" * 70,
            "CODE AUDIT REPORT",
            "=" * 70,
            "",
        ]

        for issue in self.issues:
            lines.append(str(issue))
            lines.append("")

        lines.append("=" * 70)

        report = "\n".join(lines)
        if verbose:
            print(report)

        return report


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def quick_audit(fig, axes=None, journal='default') -> List[Issue]:
    """
    Quick audit of a figure.

    Args:
        fig: matplotlib Figure
        axes: Axes array (optional)
        journal: Journal name

    Returns:
        List of issues
    """
    auditor = FigureAuditor(journal=journal)
    return auditor.audit_figure(fig, axes)


def audit_and_report(fig, axes=None, journal='default') -> None:
    """Audit figure and print report."""
    auditor = FigureAuditor(journal=journal)
    auditor.audit_figure(fig, axes)
    auditor.report()
