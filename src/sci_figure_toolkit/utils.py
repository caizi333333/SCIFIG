"""
Utility Functions
=================

Helper functions for common figure operations.
"""

from typing import List, Tuple, Optional
from pathlib import Path
import matplotlib.pyplot as plt


def save_figure(
    fig: plt.Figure,
    filepath: str,
    formats: List[str] = ['pdf', 'png', 'svg'],
    dpi: int = 600,
    transparent: bool = False,
    verbose: bool = True
) -> List[str]:
    """
    Save figure in multiple formats.

    Args:
        fig: matplotlib Figure
        filepath: Base filepath without extension
        formats: List of format extensions
        dpi: Output resolution
        transparent: If True, use transparent background
        verbose: If True, print saved paths

    Returns:
        List of saved file paths

    Example:
        >>> save_figure(fig, 'output/figure1')
        Saved: output/figure1.pdf
        Saved: output/figure1.png
        Saved: output/figure1.svg
    """
    # Ensure directory exists
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    saved = []
    for fmt in formats:
        output_path = f"{filepath}.{fmt}"

        # Use higher DPI for raster formats
        save_dpi = dpi if fmt in ['png', 'jpg', 'jpeg', 'tiff'] else None

        fig.savefig(
            output_path,
            dpi=save_dpi,
            bbox_inches='tight',
            transparent=transparent,
            facecolor=fig.get_facecolor() if not transparent else 'none',
            edgecolor='none'
        )

        saved.append(output_path)
        if verbose:
            print(f"Saved: {output_path}")

    return saved


def collect_legend_handles(
    axes: List[plt.Axes],
    deduplicate: bool = True
) -> Tuple[List, List[str]]:
    """
    Collect legend handles and labels from multiple axes.

    Args:
        axes: List of matplotlib Axes
        deduplicate: If True, remove duplicate labels

    Returns:
        (handles, labels) tuple
    """
    all_handles = []
    all_labels = []

    for ax in axes:
        handles, labels = ax.get_legend_handles_labels()
        all_handles.extend(handles)
        all_labels.extend(labels)

    if deduplicate:
        seen = set()
        unique_handles = []
        unique_labels = []
        for h, l in zip(all_handles, all_labels):
            if l not in seen:
                seen.add(l)
                unique_handles.append(h)
                unique_labels.append(l)
        return unique_handles, unique_labels

    return all_handles, all_labels


def remove_individual_legends(axes: List[plt.Axes]) -> int:
    """
    Remove legend from each individual axes.

    Args:
        axes: List of matplotlib Axes

    Returns:
        Number of legends removed
    """
    count = 0
    for ax in axes:
        legend = ax.get_legend()
        if legend is not None:
            legend.remove()
            count += 1
    return count


def set_subplot_labels(
    axes: List[plt.Axes],
    start: str = 'a',
    fmt: str = '({label})',
    fontsize: int = 9,
    fontweight: str = 'bold',
    loc: str = 'upper left'
) -> None:
    """
    Add (a), (b), (c), ... labels to subplots.

    Args:
        axes: List of Axes
        start: Starting letter
        fmt: Format string with {label} placeholder
        fontsize: Label font size
        fontweight: Label font weight
        loc: Label location ('upper left', 'upper right', etc.)
    """
    loc_coords = {
        'upper left': (0.02, 0.98),
        'upper right': (0.98, 0.98),
        'lower left': (0.02, 0.02),
        'lower right': (0.98, 0.02),
    }

    ha_map = {'left': 'left', 'right': 'right'}
    va_map = {'upper': 'top', 'lower': 'bottom'}

    x, y = loc_coords.get(loc, loc_coords['upper left'])
    ha = ha_map.get(loc.split()[1], 'left')
    va = va_map.get(loc.split()[0], 'top')

    for i, ax in enumerate(axes):
        label = chr(ord(start) + i)
        text = fmt.format(label=label)
        ax.text(x, y, text, transform=ax.transAxes,
                fontsize=fontsize, fontweight=fontweight,
                ha=ha, va=va)


def inches_to_mm(inches: float) -> float:
    """Convert inches to millimeters."""
    return inches * 25.4


def mm_to_inches(mm: float) -> float:
    """Convert millimeters to inches."""
    return mm / 25.4


def cm_to_inches(cm: float) -> float:
    """Convert centimeters to inches."""
    return cm / 2.54


def format_scientific(value: float, precision: int = 2) -> str:
    """
    Format number in scientific notation.

    Args:
        value: Number to format
        precision: Number of decimal places

    Returns:
        Formatted string
    """
    if value == 0:
        return "0"

    import math
    exp = math.floor(math.log10(abs(value)))
    mantissa = value / (10 ** exp)

    if exp == 0:
        return f"{value:.{precision}f}"
    else:
        return f"{mantissa:.{precision}f}×10^{exp}"


def colorblind_palette(n: int = 8) -> List[str]:
    """
    Get colorblind-safe color palette.

    Based on Wong, B. (2011). Nature Methods.

    Args:
        n: Number of colors needed

    Returns:
        List of hex color codes
    """
    palette = [
        '#0072B2',  # Blue
        '#D55E00',  # Vermillion
        '#009E73',  # Bluish green
        '#CC79A7',  # Reddish purple
        '#F0E442',  # Yellow
        '#56B4E9',  # Sky blue
        '#E69F00',  # Orange
        '#000000',  # Black
    ]
    return palette[:n]
