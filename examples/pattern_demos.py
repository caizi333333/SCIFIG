#!/usr/bin/env python3
"""
Design Pattern Demonstrations

This script demonstrates each design pattern with before/after comparisons:
- Pattern B: Unified Bottom Legend
- Pattern E: Title Annotations
- Pattern F: Inline Labels
- Smart Bar Labels
"""

import numpy as np
import matplotlib.pyplot as plt
from sci_figure_toolkit import (
    set_style,
    UnifiedLegend,
    TitleAnnotation,
    InlineLabel,
    smart_bar_labels,
    save_figure,
    colorblind_palette,
    JournalStandard,
)


def demo_pattern_b():
    """
    Pattern B: Unified Bottom Legend

    Problem: Multiple subplots with identical legends
    Solution: Single legend at bottom of figure
    """
    print("\n" + "=" * 50)
    print("PATTERN B: Unified Bottom Legend")
    print("=" * 50)

    set_style(JournalStandard.NATURE)
    colors = colorblind_palette(3)

    # BEFORE: Redundant legends
    fig_before, axes = plt.subplots(1, 3, figsize=(7, 2.5))
    x = np.linspace(0, 10, 50)

    for i, ax in enumerate(axes):
        ax.plot(x, np.sin(x + i), '-', color=colors[0], label='Series A')
        ax.plot(x, np.cos(x + i), '--', color=colors[1], label='Series B')
        ax.set_title(f'({chr(97+i)}) Panel {i+1}')
        ax.legend()  # ❌ Redundant!

    plt.tight_layout()
    fig_before.suptitle('BEFORE: Redundant Legends', fontsize=10, y=1.02)
    save_figure(fig_before, 'output/pattern_b_before', formats=['png'], verbose=False)

    # AFTER: Unified legend
    fig_after, axes = plt.subplots(1, 3, figsize=(7, 2.5))

    handles, labels = [], []
    for i, ax in enumerate(axes):
        h1, = ax.plot(x, np.sin(x + i), '-', color=colors[0], label='Series A')
        h2, = ax.plot(x, np.cos(x + i), '--', color=colors[1], label='Series B')
        ax.set_title(f'({chr(97+i)}) Panel {i+1}')
        if i == 0:
            handles = [h1, h2]
            labels = ['Series A', 'Series B']
        # NO individual legend

    # Apply Pattern B
    fig_after.legend(handles, labels,
                     loc='lower center',
                     bbox_to_anchor=(0.5, -0.02),
                     ncol=2, frameon=True)
    plt.tight_layout(rect=[0, 0.1, 1, 1])
    fig_after.suptitle('AFTER: Unified Legend (Pattern B)', fontsize=10, y=1.02)
    save_figure(fig_after, 'output/pattern_b_after', formats=['png'], verbose=False)

    print("✅ Saved: output/pattern_b_before.png")
    print("✅ Saved: output/pattern_b_after.png")
    plt.close('all')


def demo_pattern_e():
    """
    Pattern E: Title Annotations

    Problem: In-figure annotations blocking data
    Solution: Move annotations to title
    """
    print("\n" + "=" * 50)
    print("PATTERN E: Title Annotations")
    print("=" * 50)

    set_style(JournalStandard.NATURE)

    x = np.linspace(0, 10, 100)
    y = np.log(x + 1) + np.random.normal(0, 0.1, len(x))
    optimal_value = 3.14

    # BEFORE: Annotation blocking data
    fig_before, ax = plt.subplots(figsize=(4, 3))
    ax.plot(x, y, 'o', markersize=3, alpha=0.6)
    ax.plot(x, np.log(x + 1), 'r-', linewidth=1.5)

    # ❌ Yellow box that might block data
    ax.annotate(f'Optimal = {optimal_value:.2f}',
                xy=(5, 1.5), fontsize=10,
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    ax.set_title('(a) L-curve Analysis')
    ax.set_xlabel('Parameter')
    ax.set_ylabel('Value')
    plt.tight_layout()
    fig_before.suptitle('BEFORE: In-figure Annotation', fontsize=10, y=1.02)
    save_figure(fig_before, 'output/pattern_e_before', formats=['png'], verbose=False)

    # AFTER: Value in title
    fig_after, ax = plt.subplots(figsize=(4, 3))
    ax.plot(x, y, 'o', markersize=3, alpha=0.6)
    ax.plot(x, np.log(x + 1), 'r-', linewidth=1.5)

    # ✅ Pattern E: Move to title
    title = TitleAnnotation.format(
        main_title='(a) L-curve Analysis',
        values={'Optimal λ': optimal_value}
    )
    ax.set_title(title)
    ax.set_xlabel('Parameter')
    ax.set_ylabel('Value')
    plt.tight_layout()
    fig_after.suptitle('AFTER: Title Annotation (Pattern E)', fontsize=10, y=1.05)
    save_figure(fig_after, 'output/pattern_e_after', formats=['png'], verbose=False)

    print("✅ Saved: output/pattern_e_before.png")
    print("✅ Saved: output/pattern_e_after.png")
    plt.close('all')


def demo_pattern_f():
    """
    Pattern F: Inline Labels

    Problem: Reference line labels blocking data
    Solution: Labels inline with reference lines
    """
    print("\n" + "=" * 50)
    print("PATTERN F: Inline Labels")
    print("=" * 50)

    set_style(JournalStandard.NATURE)
    np.random.seed(42)

    x = np.linspace(0, 10, 50)
    residuals = np.random.normal(0, 1, len(x))
    sigma = np.std(residuals)

    # BEFORE: Text label blocking data
    fig_before, ax = plt.subplots(figsize=(5, 3))
    ax.scatter(x, residuals, s=20, alpha=0.6)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axhline(3*sigma, color='red', linestyle='--', linewidth=0.8)
    ax.axhline(-3*sigma, color='red', linestyle='--', linewidth=0.8)

    # ❌ Label in corner might block data
    ax.text(0.02, 0.98, r'$\pm 3\sigma$ bounds shown',
            transform=ax.transAxes, fontsize=9,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.set_xlabel('X')
    ax.set_ylabel('Residual')
    ax.set_title('Residual Plot')
    plt.tight_layout()
    fig_before.suptitle('BEFORE: Corner Text Label', fontsize=10, y=1.02)
    save_figure(fig_before, 'output/pattern_f_before', formats=['png'], verbose=False)

    # AFTER: Inline labels
    fig_after, ax = plt.subplots(figsize=(5, 3))
    ax.scatter(x, residuals, s=20, alpha=0.6)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axhline(3*sigma, color='red', linestyle='--', linewidth=0.8)
    ax.axhline(-3*sigma, color='red', linestyle='--', linewidth=0.8)

    # ✅ Pattern F: Inline labels
    InlineLabel.add(ax, y=3*sigma, label=r'$+3\sigma$', position='right', color='red')
    InlineLabel.add(ax, y=-3*sigma, label=r'$-3\sigma$', position='right', color='red')

    ax.set_xlabel('X')
    ax.set_ylabel('Residual')
    ax.set_title('Residual Plot')
    plt.tight_layout()
    fig_after.suptitle('AFTER: Inline Labels (Pattern F)', fontsize=10, y=1.02)
    save_figure(fig_after, 'output/pattern_f_after', formats=['png'], verbose=False)

    print("✅ Saved: output/pattern_f_before.png")
    print("✅ Saved: output/pattern_f_after.png")
    plt.close('all')


def demo_smart_bar_labels():
    """
    Smart Bar Labels

    Problem: Negative bar labels invisible (white text on short bars)
    Solution: Intelligent label placement based on bar height
    """
    print("\n" + "=" * 50)
    print("SMART BAR LABELS")
    print("=" * 50)

    set_style(JournalStandard.NATURE)

    features = ['Feature A', 'Feature B', 'Feature C', 'Feature D', 'Feature E']
    values = [0.85, 0.72, -0.08, 0.65, -0.15]
    colors = ['#0072B2' if v >= 0 else '#D55E00' for v in values]

    # BEFORE: Labels inside bars (problematic for short/negative bars)
    fig_before, ax = plt.subplots(figsize=(5, 4))
    bars = ax.barh(features, values, color=colors)

    # ❌ Labels inside bars - invisible on short bars!
    for bar, val in zip(bars, values):
        width = bar.get_width()
        ax.text(width/2, bar.get_y() + bar.get_height()/2,
                f'{val:.2f}', ha='center', va='center',
                color='white', fontweight='bold', fontsize=9)

    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_xlabel('Importance')
    ax.set_xlim(-0.3, 1.0)
    plt.tight_layout()
    fig_before.suptitle('BEFORE: Labels Inside Bars', fontsize=10, y=1.02)
    save_figure(fig_before, 'output/smart_labels_before', formats=['png'], verbose=False)

    # AFTER: Smart label placement
    fig_after, ax = plt.subplots(figsize=(5, 4))
    bars = ax.barh(features, values, color=colors)

    # ✅ Smart labels - outside for negative/short bars
    smart_bar_labels(ax, bars, values, orientation='horizontal', fmt='{:.2f}')

    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_xlabel('Importance')
    ax.set_xlim(-0.3, 1.0)
    plt.tight_layout()
    fig_after.suptitle('AFTER: Smart Label Placement', fontsize=10, y=1.02)
    save_figure(fig_after, 'output/smart_labels_after', formats=['png'], verbose=False)

    print("✅ Saved: output/smart_labels_before.png")
    print("✅ Saved: output/smart_labels_after.png")
    plt.close('all')


def main():
    """Run all pattern demonstrations."""
    print("\n" + "=" * 60)
    print("SCI Figure Toolkit - Design Pattern Demonstrations")
    print("=" * 60)

    # Create output directory
    import os
    os.makedirs('output', exist_ok=True)

    # Run all demos
    demo_pattern_b()
    demo_pattern_e()
    demo_pattern_f()
    demo_smart_bar_labels()

    print("\n" + "=" * 60)
    print("All demonstrations complete!")
    print("Check the 'output' directory for before/after comparisons.")
    print("=" * 60)


if __name__ == '__main__':
    main()
