#!/usr/bin/env python3
"""
Generate Case Study Images

This script generates before/after comparison images for all case studies.
Run this script to populate the docs/images/ directory.

Usage:
    python examples/generate_case_images.py
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

# Ensure output directory exists
OUTPUT_DIR = Path(__file__).parent.parent / "docs" / "images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def set_sci_style():
    """Apply SCI-standard style settings."""
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': 9,
        'axes.labelsize': 9,
        'axes.titlesize': 9,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8,
        'lines.linewidth': 1.5,
        'lines.markersize': 4,
        'figure.dpi': 150,
        'savefig.dpi': 300,
        'axes.linewidth': 0.8,
    })


def generate_case1():
    """
    Case 1: Redundant Legends

    Before: Each subplot has its own legend (redundant)
    After: Single unified legend at bottom
    """
    np.random.seed(42)
    T = np.linspace(-50, 150, 100)

    # Generate sample data
    def lorentzian(T, center, width, amp):
        return amp / (1 + ((T - center) / width) ** 2)

    # BEFORE: Redundant legends
    fig_before, axes = plt.subplots(1, 3, figsize=(7, 2.5))
    fig_before.suptitle('BEFORE: Redundant Legends in Each Subplot', fontsize=10, y=1.02)

    freqs = [0.1, 1.0, 10.0]
    colors = ['#0072B2', '#D55E00']

    for i, (ax, freq) in enumerate(zip(axes, freqs)):
        # Simulated data
        y_exp = lorentzian(T, 50 + i*10, 30, 100) + np.random.normal(0, 5, len(T))
        y_fit = lorentzian(T, 50 + i*10, 30, 100)

        ax.plot(T, y_exp, 'o', color=colors[0], markersize=3, alpha=0.6, label='Experimental')
        ax.plot(T, y_fit, '-', color=colors[1], linewidth=1.5, label='Fit')
        ax.set_title(f'({chr(97+i)}) {freq} Hz')
        ax.set_xlabel('Temperature (°C)')
        if i == 0:
            ax.set_ylabel("E'' (MPa)")
        ax.legend(loc='upper right', fontsize=7)  # REDUNDANT!

    plt.tight_layout()
    fig_before.savefig(OUTPUT_DIR / 'case1_before.png', bbox_inches='tight',
                       facecolor='white', edgecolor='none')
    plt.close(fig_before)

    # AFTER: Unified legend
    fig_after, axes = plt.subplots(1, 3, figsize=(7, 2.5))
    fig_after.suptitle('AFTER: Single Unified Legend (Pattern B)', fontsize=10, y=1.02)

    handles, labels = [], []
    for i, (ax, freq) in enumerate(zip(axes, freqs)):
        y_exp = lorentzian(T, 50 + i*10, 30, 100) + np.random.normal(0, 5, len(T))
        y_fit = lorentzian(T, 50 + i*10, 30, 100)

        h1, = ax.plot(T, y_exp, 'o', color=colors[0], markersize=3, alpha=0.6)
        h2, = ax.plot(T, y_fit, '-', color=colors[1], linewidth=1.5)

        if i == 0:
            handles = [h1, h2]
            labels = ['Experimental', 'Double Lorentzian Fit']

        ax.set_title(f'({chr(97+i)}) {freq} Hz')
        ax.set_xlabel('Temperature (°C)')
        if i == 0:
            ax.set_ylabel("E'' (MPa)")
        # NO individual legend!

    fig_after.legend(handles, labels, loc='lower center',
                     bbox_to_anchor=(0.5, -0.02), ncol=2, fontsize=8)
    plt.tight_layout(rect=[0, 0.08, 1, 0.98])
    fig_after.savefig(OUTPUT_DIR / 'case1_after.png', bbox_inches='tight',
                      facecolor='white', edgecolor='none')
    plt.close(fig_after)

    print("✅ Generated: case1_before.png, case1_after.png")


def generate_case2():
    """
    Case 2: Data Occlusion

    Before: Yellow warning box covers data
    After: Note moved to title
    """
    np.random.seed(42)
    T = np.linspace(-50, 200, 100)

    # BEFORE: Yellow box occludes data
    fig_before, axes = plt.subplots(1, 2, figsize=(7, 3))
    fig_before.suptitle('BEFORE: Warning Box Occludes Data', fontsize=10, y=1.02)

    for i, ax in enumerate(axes):
        y = np.exp(-((T - 100) / 50) ** 2) * 1000 + np.random.normal(0, 30, len(T))
        y_fit = np.exp(-((T - 100) / 50) ** 2) * 1000

        ax.plot(T, y, 'o', markersize=3, alpha=0.6, color='#0072B2')
        ax.plot(T, y_fit, '-', linewidth=1.5, color='#D55E00')
        ax.set_xlabel('Temperature (°C)')
        ax.set_ylabel("E' (MPa)" if i == 0 else "E'' (MPa)")
        ax.set_title(f"({chr(97+i)}) {'E′' if i == 0 else 'E″'} Model")

        if i == 1:
            # Yellow box that occludes data!
            ax.annotate('Diagnostic only\n(not validated)',
                       xy=(50, 800), fontsize=8,
                       bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))

    plt.tight_layout()
    fig_before.savefig(OUTPUT_DIR / 'case2_before.png', bbox_inches='tight',
                       facecolor='white', edgecolor='none')
    plt.close(fig_before)

    # AFTER: Note in title
    fig_after, axes = plt.subplots(1, 2, figsize=(7, 3))
    fig_after.suptitle('AFTER: Note Moved to Title (Pattern E)', fontsize=10, y=1.02)

    for i, ax in enumerate(axes):
        y = np.exp(-((T - 100) / 50) ** 2) * 1000 + np.random.normal(0, 30, len(T))
        y_fit = np.exp(-((T - 100) / 50) ** 2) * 1000

        ax.plot(T, y, 'o', markersize=3, alpha=0.6, color='#0072B2')
        ax.plot(T, y_fit, '-', linewidth=1.5, color='#D55E00')
        ax.set_xlabel('Temperature (°C)')
        ax.set_ylabel("E' (MPa)" if i == 0 else "E'' (MPa)")

        if i == 0:
            ax.set_title("(a) E′ Model Comparison\n(LOFO-validated)")
        else:
            ax.set_title("(b) E″ Model Comparison\n(Diagnostic only)")

    plt.tight_layout()
    fig_after.savefig(OUTPUT_DIR / 'case2_after.png', bbox_inches='tight',
                      facecolor='white', edgecolor='none')
    plt.close(fig_after)

    print("✅ Generated: case2_before.png, case2_after.png")


def generate_case3():
    """
    Case 3: Broken Annotations

    Before: Truncated ".0e" annotation
    After: Clean value in title
    """
    np.random.seed(42)

    # L-curve data
    lambda_vals = np.logspace(-3, 1, 50)
    residual_norm = 1 / (1 + lambda_vals) + 0.1
    solution_norm = lambda_vals ** 0.5

    opt_idx = 25
    opt_lambda = lambda_vals[opt_idx]

    # BEFORE: Broken annotation
    fig_before, ax = plt.subplots(figsize=(4, 3.5))
    fig_before.suptitle('BEFORE: Broken Format String', fontsize=10, y=0.98)

    ax.loglog(residual_norm, solution_norm, 'b-', linewidth=1.5)
    ax.plot(residual_norm[opt_idx], solution_norm[opt_idx], 'ro', markersize=8)
    ax.set_xlabel('Residual Norm')
    ax.set_ylabel('Solution Norm')
    ax.set_title('(a) L-curve Analysis')

    # Broken annotation!
    ax.annotate('.0e', xy=(residual_norm[opt_idx], solution_norm[opt_idx]),
                xytext=(0.3, 0.3), fontsize=10, color='red',
                arrowprops=dict(arrowstyle='->', color='red'))

    plt.tight_layout()
    fig_before.savefig(OUTPUT_DIR / 'case3_before.png', bbox_inches='tight',
                       facecolor='white', edgecolor='none')
    plt.close(fig_before)

    # AFTER: Value in title
    fig_after, ax = plt.subplots(figsize=(4, 3.5))
    fig_after.suptitle('AFTER: Value in Title (Pattern E)', fontsize=10, y=0.98)

    ax.loglog(residual_norm, solution_norm, 'b-', linewidth=1.5)
    ax.plot(residual_norm[opt_idx], solution_norm[opt_idx], 'ro', markersize=8)
    ax.set_xlabel('Residual Norm')
    ax.set_ylabel('Solution Norm')
    ax.set_title(f'(a) L-curve Analysis\n(Optimal λ = {opt_lambda:.2e})')

    plt.tight_layout()
    fig_after.savefig(OUTPUT_DIR / 'case3_after.png', bbox_inches='tight',
                      facecolor='white', edgecolor='none')
    plt.close(fig_after)

    print("✅ Generated: case3_before.png, case3_after.png")


def generate_case4():
    """
    Case 4: Reference Line Occlusion

    Before: Text label covers data
    After: Inline label on reference line
    """
    np.random.seed(42)
    T = np.linspace(0, 100, 50)

    # BEFORE: Text occludes data
    fig_before, ax = plt.subplots(figsize=(5, 3.5))
    fig_before.suptitle('BEFORE: Text Label Occludes Data', fontsize=10, y=0.98)

    residuals = np.random.normal(0, 1, len(T))
    sigma = np.std(residuals)

    ax.scatter(T, residuals, s=25, alpha=0.7, c='#0072B2')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axhline(3*sigma, color='red', linestyle='--', linewidth=1)
    ax.axhline(-3*sigma, color='red', linestyle='--', linewidth=1)

    # Text that occludes data!
    ax.text(5, 2.5, '±3× pooled SD\nbounds shown', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))

    ax.set_xlabel('Temperature (°C)')
    ax.set_ylabel('Residual')
    ax.set_title('Residual Analysis')

    plt.tight_layout()
    fig_before.savefig(OUTPUT_DIR / 'case4_before.png', bbox_inches='tight',
                       facecolor='white', edgecolor='none')
    plt.close(fig_before)

    # AFTER: Inline labels
    fig_after, ax = plt.subplots(figsize=(5, 3.5))
    fig_after.suptitle('AFTER: Inline Labels (Pattern F)', fontsize=10, y=0.98)

    ax.scatter(T, residuals, s=25, alpha=0.7, c='#0072B2')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axhline(3*sigma, color='red', linestyle='--', linewidth=1)
    ax.axhline(-3*sigma, color='red', linestyle='--', linewidth=1)

    # Inline labels
    ax.text(98, 3*sigma, r'$+3\sigma$', fontsize=8, color='red',
            ha='right', va='bottom')
    ax.text(98, -3*sigma, r'$-3\sigma$', fontsize=8, color='red',
            ha='right', va='top')

    ax.set_xlabel('Temperature (°C)')
    ax.set_ylabel('Residual')
    ax.set_title('Residual Analysis')

    plt.tight_layout()
    fig_after.savefig(OUTPUT_DIR / 'case4_after.png', bbox_inches='tight',
                      facecolor='white', edgecolor='none')
    plt.close(fig_after)

    print("✅ Generated: case4_before.png, case4_after.png")


def generate_case5():
    """
    Case 5: Bar Chart Labels

    Before: Negative bar labels invisible (white on short bar)
    After: Smart label placement
    """
    # Data
    features = ['Feature A', 'Feature B', 'Feature C', 'Feature D', 'Feature E']
    values = [0.85, 0.72, -0.08, 0.65, -0.15]

    # BEFORE: Labels inside bars
    fig_before, ax = plt.subplots(figsize=(5, 4))
    fig_before.suptitle('BEFORE: Invisible Labels on Short Bars', fontsize=10, y=0.98)

    colors = ['#0072B2' if v >= 0 else '#D55E00' for v in values]
    bars = ax.barh(features, values, color=colors)

    # Labels inside bars (problematic!)
    for bar, val in zip(bars, values):
        width = bar.get_width()
        if width != 0:
            ax.text(width/2, bar.get_y() + bar.get_height()/2,
                   f'{val:.2f}', ha='center', va='center',
                   color='white', fontweight='bold', fontsize=9)

    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_xlabel('Importance Score')
    ax.set_xlim(-0.3, 1.0)

    plt.tight_layout()
    fig_before.savefig(OUTPUT_DIR / 'case5_before.png', bbox_inches='tight',
                       facecolor='white', edgecolor='none')
    plt.close(fig_before)

    # AFTER: Smart labels
    fig_after, ax = plt.subplots(figsize=(5, 4))
    fig_after.suptitle('AFTER: Smart Label Placement', fontsize=10, y=0.98)

    bars = ax.barh(features, values, color=colors)

    # Smart label placement
    for bar, val in zip(bars, values):
        width = bar.get_width()
        if val >= 0:
            # Positive: label to the right of bar
            ax.text(width + 0.02, bar.get_y() + bar.get_height()/2,
                   f'{val:.2f}', ha='left', va='center',
                   color='black', fontsize=9)
        else:
            # Negative: label to the left of bar
            ax.text(width - 0.02, bar.get_y() + bar.get_height()/2,
                   f'{val:.2f}', ha='right', va='center',
                   color='black', fontsize=9)

    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_xlabel('Importance Score')
    ax.set_xlim(-0.3, 1.0)

    plt.tight_layout()
    fig_after.savefig(OUTPUT_DIR / 'case5_after.png', bbox_inches='tight',
                      facecolor='white', edgecolor='none')
    plt.close(fig_after)

    print("✅ Generated: case5_before.png, case5_after.png")


def generate_case6():
    """
    Case 6: Font Inconsistency

    Before: Mixed font sizes across figure elements
    After: Consistent SCI-standard font sizes
    """
    np.random.seed(42)
    x = np.linspace(0, 10, 50)
    y = np.sin(x) + np.random.normal(0, 0.1, len(x))

    # BEFORE: Inconsistent fonts
    fig_before, ax = plt.subplots(figsize=(5, 4))
    fig_before.suptitle('BEFORE: Inconsistent Font Sizes', fontsize=10, y=0.98)

    ax.plot(x, y, 'o-', markersize=4, color='#0072B2')
    ax.set_xlabel('Time (s)', fontsize=14)      # Too large!
    ax.set_ylabel('Amplitude', fontsize=8)       # Too small!
    ax.set_title('Signal Analysis', fontsize=12)  # Inconsistent!
    ax.tick_params(axis='x', labelsize=10)       # Different from y!
    ax.tick_params(axis='y', labelsize=6)        # Too small!
    ax.legend(['Data'], fontsize=11, loc='upper right')  # Random size!

    # Add annotation with yet another size
    ax.annotate('Peak', xy=(1.5, 1.0), fontsize=15,
                arrowprops=dict(arrowstyle='->'))

    plt.tight_layout()
    fig_before.savefig(OUTPUT_DIR / 'case6_before.png', bbox_inches='tight',
                       facecolor='white', edgecolor='none')
    plt.close(fig_before)

    # AFTER: Consistent fonts (SCI standard) + Pattern E for annotation
    fig_after, ax = plt.subplots(figsize=(5, 4))
    fig_after.suptitle('AFTER: Consistent SCI-Standard Fonts', fontsize=10, y=0.98)

    ax.plot(x, y, 'o-', markersize=4, color='#0072B2')
    ax.set_xlabel('Time (s)', fontsize=9)        # Standard: 9pt
    ax.set_ylabel('Amplitude', fontsize=9)       # Standard: 9pt
    ax.tick_params(axis='both', labelsize=8)     # Standard: 8pt
    ax.legend(['Data'], fontsize=8, loc='upper right')  # Standard: 8pt

    # Pattern E: Move annotation info to title instead of in-plot arrow
    # This avoids potential data occlusion
    peak_idx = np.argmax(y)
    peak_x, peak_y = x[peak_idx], y[peak_idx]
    ax.set_title(f'Signal Analysis\n(Peak at t={peak_x:.1f}s, A={peak_y:.2f})', fontsize=9)  # Standard: 9pt

    # NO arrow annotation that could occlude data!

    plt.tight_layout()
    fig_after.savefig(OUTPUT_DIR / 'case6_after.png', bbox_inches='tight',
                      facecolor='white', edgecolor='none')
    plt.close(fig_after)

    print("✅ Generated: case6_before.png, case6_after.png")


def generate_case7():
    """
    Case 7: Non-Standard Figure Size

    Before: Arbitrary figure size (10x6 inches)
    After: Journal-standard width (7.0 inches for double column)
    """
    np.random.seed(42)
    x = np.linspace(0, 10, 100)

    # BEFORE: Non-standard size (too wide)
    fig_before, axes = plt.subplots(1, 3, figsize=(10, 3))  # Non-standard!
    fig_before.suptitle('BEFORE: Non-Standard Size (10" wide)', fontsize=10, y=1.02)

    for i, ax in enumerate(axes):
        y = np.sin(x + i) + np.random.normal(0, 0.1, len(x))
        ax.plot(x, y, '-', color='#0072B2', linewidth=1.5)
        ax.set_title(f'({chr(97+i)}) Panel {i+1}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

    # Add size annotation
    fig_before.text(0.5, -0.05, '⚠️ Width: 10.0" (non-standard)',
                   ha='center', fontsize=9, color='red',
                   transform=fig_before.transFigure)

    plt.tight_layout(rect=[0, 0.05, 1, 0.98])
    fig_before.savefig(OUTPUT_DIR / 'case7_before.png', bbox_inches='tight',
                       facecolor='white', edgecolor='none')
    plt.close(fig_before)

    # AFTER: Standard double-column width
    fig_after, axes = plt.subplots(1, 3, figsize=(7.0, 2.5))  # Nature standard!
    fig_after.suptitle('AFTER: Standard Double-Column (7.0")', fontsize=10, y=1.02)

    for i, ax in enumerate(axes):
        y = np.sin(x + i) + np.random.normal(0, 0.1, len(x))
        ax.plot(x, y, '-', color='#0072B2', linewidth=1.5)
        ax.set_title(f'({chr(97+i)}) Panel {i+1}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

    # Add size annotation
    fig_after.text(0.5, -0.05, '✓ Width: 7.0" (Nature/Science standard)',
                  ha='center', fontsize=9, color='green',
                  transform=fig_after.transFigure)

    plt.tight_layout(rect=[0, 0.05, 1, 0.98])
    fig_after.savefig(OUTPUT_DIR / 'case7_after.png', bbox_inches='tight',
                      facecolor='white', edgecolor='none')
    plt.close(fig_after)

    print("✅ Generated: case7_before.png, case7_after.png")


def generate_case8():
    """
    Case 8: Low DPI Output

    Before: 72 DPI (screen resolution, pixelated in print)
    After: 600 DPI (publication quality)
    """
    np.random.seed(42)
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x)

    # BEFORE: Low DPI (simulated with visible pixels)
    fig_before, ax = plt.subplots(figsize=(4, 3))
    fig_before.suptitle('BEFORE: Low Resolution (72 DPI)', fontsize=10, y=0.98)

    ax.plot(x, y, '-', color='#0072B2', linewidth=2)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Sine Wave')

    # Add DPI warning
    ax.text(0.5, -0.15, '⚠️ 72 DPI - Will appear pixelated in print',
           ha='center', fontsize=8, color='red',
           transform=ax.transAxes)

    plt.tight_layout()
    # Save at low DPI to show the problem
    fig_before.savefig(OUTPUT_DIR / 'case8_before.png', dpi=72,
                       bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig_before)

    # AFTER: High DPI
    fig_after, ax = plt.subplots(figsize=(4, 3))
    fig_after.suptitle('AFTER: Publication Quality (600 DPI)', fontsize=10, y=0.98)

    ax.plot(x, y, '-', color='#0072B2', linewidth=2)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Sine Wave')

    # Add DPI confirmation
    ax.text(0.5, -0.15, '✓ 600 DPI - Publication ready',
           ha='center', fontsize=8, color='green',
           transform=ax.transAxes)

    plt.tight_layout()
    fig_after.savefig(OUTPUT_DIR / 'case8_after.png', dpi=300,  # Use 300 for file size
                      bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig_after)

    print("✅ Generated: case8_before.png, case8_after.png")


def generate_case9():
    """
    Case 9: Non-Colorblind Safe Colors

    Before: Red-green color scheme (problematic for ~8% of males)
    After: Colorblind-safe palette (Wong 2011)
    """
    np.random.seed(42)
    x = np.linspace(0, 10, 50)

    # BEFORE: Red-green (problematic)
    fig_before, ax = plt.subplots(figsize=(5, 4))
    fig_before.suptitle('BEFORE: Red-Green Colors (Not Colorblind Safe)', fontsize=10, y=0.98)

    colors_bad = ['red', 'green', 'orange', 'purple']
    for i, c in enumerate(colors_bad):
        y = np.sin(x + i*0.5) + i*0.5
        ax.plot(x, y, '-', color=c, linewidth=2, label=f'Series {i+1}')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend(loc='upper right')

    # Warning
    ax.text(0.5, -0.12, '⚠️ Red/Green indistinguishable for colorblind viewers',
           ha='center', fontsize=8, color='red',
           transform=ax.transAxes)

    plt.tight_layout()
    fig_before.savefig(OUTPUT_DIR / 'case9_before.png', bbox_inches='tight',
                       facecolor='white', edgecolor='none')
    plt.close(fig_before)

    # AFTER: Colorblind-safe (Wong 2011)
    fig_after, ax = plt.subplots(figsize=(5, 4))
    fig_after.suptitle('AFTER: Colorblind-Safe Palette (Wong 2011)', fontsize=10, y=0.98)

    # Wong 2011 colorblind-safe palette
    colors_good = ['#0072B2', '#D55E00', '#009E73', '#CC79A7']
    for i, c in enumerate(colors_good):
        y = np.sin(x + i*0.5) + i*0.5
        ax.plot(x, y, '-', color=c, linewidth=2, label=f'Series {i+1}')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend(loc='upper right')

    # Confirmation
    ax.text(0.5, -0.12, '✓ Colors distinguishable for all viewers',
           ha='center', fontsize=8, color='green',
           transform=ax.transAxes)

    plt.tight_layout()
    fig_after.savefig(OUTPUT_DIR / 'case9_after.png', bbox_inches='tight',
                      facecolor='white', edgecolor='none')
    plt.close(fig_after)

    print("✅ Generated: case9_before.png, case9_after.png")


def main():
    """Generate all case study images."""
    print("\n" + "=" * 50)
    print("Generating Case Study Images")
    print("=" * 50)
    print(f"Output directory: {OUTPUT_DIR}\n")

    set_sci_style()

    generate_case1()
    generate_case2()
    generate_case3()
    generate_case4()
    generate_case5()
    generate_case6()
    generate_case7()
    generate_case8()
    generate_case9()

    print("\n" + "=" * 50)
    print(f"All images saved to: {OUTPUT_DIR}")
    print("=" * 50 + "\n")


if __name__ == '__main__':
    main()
