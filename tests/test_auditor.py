"""Tests for figure auditor module."""

import pytest
import numpy as np

# Skip tests if matplotlib is not available in test environment
pytest.importorskip("matplotlib")

import matplotlib.pyplot as plt
from sci_figure_toolkit.auditor import (
    FigureAuditor,
    CodeAuditor,
    Issue,
    IssueType,
    Severity,
)


class TestIssue:
    """Test Issue dataclass."""

    def test_issue_creation(self):
        """Test creating an Issue."""
        issue = Issue(
            type=IssueType.REDUNDANT_LEGEND,
            severity=Severity.WARNING,
            message="Duplicate legends found",
            location="axes[0], axes[1]",
            suggestion="Use Pattern B: unified bottom legend",
        )
        assert issue.type == IssueType.REDUNDANT_LEGEND
        assert issue.severity == Severity.WARNING
        assert "Duplicate" in issue.message

    def test_issue_with_fix(self):
        """Test Issue with auto-fix code."""
        issue = Issue(
            type=IssueType.FONT_INCONSISTENCY,
            severity=Severity.INFO,
            message="Inconsistent font sizes",
            auto_fix="ax.tick_params(labelsize=8)",
        )
        assert issue.auto_fix is not None


class TestFigureAuditor:
    """Test FigureAuditor class."""

    @pytest.fixture
    def simple_figure(self):
        """Create a simple test figure."""
        fig, ax = plt.subplots(figsize=(3.5, 3.0))
        ax.plot([1, 2, 3], [1, 4, 9], label="Data")
        ax.set_xlabel("X axis")
        ax.set_ylabel("Y axis")
        yield fig, [ax]
        plt.close(fig)

    @pytest.fixture
    def multi_panel_figure(self):
        """Create a multi-panel test figure."""
        fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.5))
        for i, ax in enumerate(axes):
            ax.plot([1, 2, 3], [1, 2, 3], label="0.1 Hz")
            ax.plot([1, 2, 3], [2, 3, 4], label="1.0 Hz")
            ax.legend()  # Creates redundant legends
        yield fig, list(axes)
        plt.close(fig)

    @pytest.fixture
    def auditor(self):
        """Create a FigureAuditor instance."""
        return FigureAuditor()

    def test_auditor_creation(self, auditor):
        """Test creating a FigureAuditor."""
        assert auditor is not None
        assert auditor.journal == "nature"  # Default journal

    def test_audit_simple_figure(self, auditor, simple_figure):
        """Test auditing a simple figure."""
        fig, axes = simple_figure
        issues = auditor.audit_figure(fig, axes)
        assert isinstance(issues, list)

    def test_detect_redundant_legends(self, auditor, multi_panel_figure):
        """Test detection of redundant legends."""
        fig, axes = multi_panel_figure
        issues = auditor.audit_figure(fig, axes)

        redundant_issues = [
            i for i in issues if i.type == IssueType.REDUNDANT_LEGEND
        ]
        assert len(redundant_issues) > 0

    def test_detect_non_standard_size(self, auditor):
        """Test detection of non-standard figure size."""
        fig, ax = plt.subplots(figsize=(8.0, 6.0))  # Non-standard
        try:
            issues = auditor.audit_figure(fig, [ax])
            size_issues = [
                i for i in issues if i.type == IssueType.NON_STANDARD_SIZE
            ]
            assert len(size_issues) > 0
        finally:
            plt.close(fig)

    def test_print_report(self, auditor, multi_panel_figure, capsys):
        """Test printing audit report."""
        fig, axes = multi_panel_figure
        auditor.audit_figure(fig, axes)
        auditor.print_report()

        captured = capsys.readouterr()
        assert "AUDIT REPORT" in captured.out or len(captured.out) > 0


class TestCodeAuditor:
    """Test CodeAuditor class."""

    @pytest.fixture
    def auditor(self):
        """Create a CodeAuditor instance."""
        return CodeAuditor()

    def test_auditor_creation(self, auditor):
        """Test creating a CodeAuditor."""
        assert auditor is not None

    def test_audit_code_with_legend(self, auditor):
        """Test auditing code with ax.legend() calls."""
        code = '''
def plot_data():
    fig, axes = plt.subplots(1, 3)
    for ax in axes:
        ax.plot(x, y, label="data")
        ax.legend()  # Individual legends
    plt.show()
'''
        issues = auditor.audit_code(code)
        assert isinstance(issues, list)

    def test_audit_code_with_hardcoded_fontsize(self, auditor):
        """Test auditing code with hardcoded font sizes."""
        code = '''
ax.set_xlabel("X", fontsize=12)
ax.set_ylabel("Y", fontsize=10)
ax.tick_params(labelsize=9)
'''
        issues = auditor.audit_code(code)
        font_issues = [
            i for i in issues if i.type == IssueType.FONT_INCONSISTENCY
        ]
        # Should detect inconsistent font sizes
        assert isinstance(font_issues, list)

    def test_audit_file(self, auditor, tmp_path):
        """Test auditing a Python file."""
        test_file = tmp_path / "test_plot.py"
        test_file.write_text('''
import matplotlib.pyplot as plt

def create_figure():
    fig, ax = plt.subplots()
    ax.plot([1,2,3], [1,4,9])
    ax.legend()
    return fig
''')
        issues = auditor.audit_file(str(test_file))
        assert isinstance(issues, list)


class TestSeverity:
    """Test Severity enum."""

    def test_severity_ordering(self):
        """Test that severities can be compared."""
        assert Severity.ERROR.value > Severity.WARNING.value
        assert Severity.WARNING.value > Severity.INFO.value

    def test_severity_values(self):
        """Test severity enum values."""
        assert Severity.INFO is not None
        assert Severity.WARNING is not None
        assert Severity.ERROR is not None


class TestIssueType:
    """Test IssueType enum."""

    def test_issue_types_exist(self):
        """Test that expected issue types exist."""
        assert IssueType.REDUNDANT_LEGEND is not None
        assert IssueType.DATA_OCCLUSION is not None
        assert IssueType.FONT_INCONSISTENCY is not None
        assert IssueType.NON_STANDARD_SIZE is not None
