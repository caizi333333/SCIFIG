#!/usr/bin/env python3
"""
Quick Start Example for sci-figure-toolkit

This example demonstrates the basic workflow:
1. Set journal style
2. Create a compliant figure
3. Apply design patterns
4. Audit and fix issues
5. Save in publication formats
"""

import numpy as np
import matplotlib.pyplot as plt

# Import the toolkit
from sci_figure_toolkit import (
    set_style,
    create_figure,
    get_figure_size,
    FigureAuditor,
    UnifiedLegend,
    save_figure,
    colorblind_palette,
    JournalStandard,
)


def generate_sample_data():
    """Generate sample data for demonstration."""
    np.random.seed(42)
    x = np.linspace(0, 10, 50)

    data = {
        '0.1 Hz': {
            'x': x,
            'y': np.sin(x) + np.random.normal(0, 0.1, len(x)),
            'fit': np.sin(x),
        },
        '1.0 Hz': {
            'x': x,
            'y': np.sin(2*x) + np.random.normal(0, 0.1, len(x)),
            'fit': np.sin(2*x),
        },
        '10.0 Hz': {
            'x': x,
            'y': np.sin(3*x) + np.random.normal(0, 0.1, len(x)),
            'fit': np.sin(3*x),
        },
    }
    return data


def example_before_fix():
    """
    Example: Figure with common issues (BEFORE fixing).

    Issues:
    - Redundant legends in each subplot
    - Non-standard figure size
    - Inconsistent styling
    """
    data = generate_sample_data()

    # Create figure without toolkit (common mistakes)
    fig, axes = plt.subplots(1, 3, figsize=(10, 3))  # Non-standard size!

    colors = ['blue', 'red', 'green']  # Not colorblind-safe!

    for i, (freq, d) in enumerate(data.items()):
        ax = axes[i]
        ax.scatter(d['x'], d['y'], s=20, color=colors[i], alpha=0.6, label='Data')
        ax.plot(d['x'], d['fit'], '-', color=colors[i], label='Fit')
        ax.set_xlabel('Time (s)', fontsize=12)  # Inconsistent font!
        ax.set_ylabel('Amplitude', fontsize=10)  # Different size!
        ax.set_title(f'{freq}')
        ax.legend()  # REDUNDANT legend in each subplot!

    plt.tight_layout()
    return fig


def example_after_fix():
    """
    Example: Figure with issues fixed (AFTER applying toolkit).

    Fixes applied:
    - Pattern B: Unified bottom legend
    - Standard figure size for Nature journal
    - Consistent fonts using journal style
    - Colorblind-safe palette
    """
    data = generate_sample_data()

    # 1. Set journal style
    set_style(JournalStandard.NATURE)

    # 2. Create figure with standard dimensions
    width, height = get_figure_size('double', aspect_ratio=0.35)
    fig, axes = plt.subplots(1, 3, figsize=(width, height))

    # 3. Use colorblind-safe colors
    colors = colorblind_palette(n=3)

    # Collect handles for unified legend
    handles, labels = [], []

    for i, (freq, d) in enumerate(data.items()):
        ax = axes[i]

        # Plot with consistent styling
        h1 = ax.scatter(d['x'], d['y'], s=16, color=colors[i], alpha=0.7, label='Data')
        h2, = ax.plot(d['x'], d['fit'], '-', color=colors[i], linewidth=1.5, label='Fit')

        # Collect handles from first subplot only
        if i == 0:
            handles = [h1, h2]
            labels = ['Experimental', 'Model Fit']

        # Standard labels (font sizes controlled by set_style)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.set_title(f'({chr(97+i)}) {freq}')

        # NO individual legend!

    # 4. Apply Pattern B: Unified bottom legend
    fig.legend(handles, labels,
               loc='lower center',
               bbox_to_anchor=(0.5, -0.02),
               ncol=2, frameon=True)

    plt.tight_layout(rect=[0, 0.1, 1, 1])  # Leave space for legend
    return fig


def main():
    """Main function demonstrating the toolkit workflow."""
    print("=" * 60)
    print("SCI Figure Toolkit - Quick Start Example")
    print("=" * 60)

    # Generate "before" figure with issues
    print("\n1. Creating figure with common issues...")
    fig_before = example_before_fix()

    # Audit the problematic figure
    print("\n2. Auditing the figure...")
    auditor = FigureAuditor(journal='nature')
    issues = auditor.audit_figure(fig_before, list(fig_before.axes))

    print("\n   AUDIT RESULTS (Before Fix):")
    auditor.print_report()

    # Generate "after" figure with fixes
    print("\n3. Creating fixed figure...")
    fig_after = example_after_fix()

    # Audit the fixed figure
    print("\n4. Auditing the fixed figure...")
    issues_after = auditor.audit_figure(fig_after, list(fig_after.axes))

    print("\n   AUDIT RESULTS (After Fix):")
    if len(issues_after) == 0:
        print("   ✅ No issues found! Figure is publication-ready.")
    else:
        auditor.print_report()

    # Save both versions
    print("\n5. Saving figures...")
    save_figure(fig_before, 'output/example_before', formats=['png'], dpi=150, verbose=True)
    save_figure(fig_after, 'output/example_after', formats=['png', 'pdf'], verbose=True)

    plt.close('all')
    print("\n" + "=" * 60)
    print("Done! Check the 'output' directory for generated figures.")
    print("=" * 60)


if __name__ == '__main__':
    main()
