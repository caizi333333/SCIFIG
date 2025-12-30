"""
Style Management
================

Apply journal-specific styles to matplotlib figures.

Usage:
    >>> from sci_figure_toolkit import set_style, create_figure
    >>> set_style('nature')
    >>> fig, ax = create_figure(1, 2, width='double')
"""

from typing import Tuple, Optional, List, Union
import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler

from .standards import get_standard, FigureSpec


def set_style(
    journal: str = 'default',
    use_tex: bool = False,
    context: str = 'paper'
) -> FigureSpec:
    """
    Set global matplotlib style for a journal.

    Args:
        journal: Journal name (e.g., 'nature', 'science', 'cell')
        use_tex: If True, enable LaTeX rendering (slower but better math)
        context: Style context ('paper', 'notebook', 'talk', 'poster')

    Returns:
        FigureSpec for the journal

    Example:
        >>> set_style('nature')
        >>> fig, ax = plt.subplots()
    """
    spec = get_standard(journal)

    # Scale factors for different contexts
    scale = {
        'paper': 1.0,
        'notebook': 1.2,
        'talk': 1.5,
        'poster': 2.0,
    }.get(context, 1.0)

    # Build rcParams
    params = {
        # Figure
        'figure.figsize': (spec.width_double, spec.width_double * 0.6),
        'figure.dpi': 100,
        'figure.facecolor': 'white',
        'figure.edgecolor': 'white',

        # Saving
        'savefig.dpi': spec.dpi,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.05,
        'savefig.facecolor': 'white',
        'savefig.edgecolor': 'white',

        # Font
        'font.size': spec.font_axis_label * scale,
        'font.family': spec.font_family,

        # Axes
        'axes.labelsize': spec.font_axis_label * scale,
        'axes.titlesize': spec.font_title * scale,
        'axes.titleweight': 'normal',
        'axes.linewidth': spec.line_width_axis,
        'axes.facecolor': 'white',
        'axes.edgecolor': 'black',
        'axes.grid': False,
        'axes.axisbelow': True,
        'axes.prop_cycle': cycler('color', list(spec.color_cycle)),

        # Ticks
        'xtick.labelsize': spec.font_tick_label * scale,
        'ytick.labelsize': spec.font_tick_label * scale,
        'xtick.direction': 'out',
        'ytick.direction': 'out',
        'xtick.major.size': 4,
        'ytick.major.size': 4,
        'xtick.minor.size': 2,
        'ytick.minor.size': 2,
        'xtick.major.width': spec.line_width_axis,
        'ytick.major.width': spec.line_width_axis,

        # Legend
        'legend.fontsize': spec.font_legend * scale,
        'legend.frameon': True,
        'legend.framealpha': 0.9,
        'legend.fancybox': False,
        'legend.edgecolor': '0.8',

        # Lines
        'lines.linewidth': spec.line_width_data,
        'lines.markersize': spec.marker_size_data,

        # Patches
        'patch.linewidth': spec.line_width_axis,

        # Grid (usually off for publications)
        'grid.linewidth': 0.5,
        'grid.alpha': 0.3,

        # Text
        'text.usetex': use_tex,
    }

    # Apply to matplotlib
    mpl.rcParams.update(params)

    return spec


def apply_style(
    fig: plt.Figure,
    axes: Optional[Union[plt.Axes, List[plt.Axes]]] = None,
    journal: str = 'default'
) -> None:
    """
    Apply journal style to an existing figure.

    Args:
        fig: matplotlib Figure
        axes: Optional Axes or list of Axes
        journal: Journal name

    Example:
        >>> fig, ax = plt.subplots()
        >>> # ... plotting ...
        >>> apply_style(fig, ax, journal='nature')
    """
    spec = get_standard(journal)

    # Get axes
    if axes is None:
        axes = fig.get_axes()
    elif not isinstance(axes, list):
        axes = [axes]

    # Apply to each axes
    for ax in axes:
        # Font sizes
        ax.title.set_fontsize(spec.font_title)
        ax.xaxis.label.set_fontsize(spec.font_axis_label)
        ax.yaxis.label.set_fontsize(spec.font_axis_label)

        # Tick labels
        ax.tick_params(labelsize=spec.font_tick_label)

        # Spine widths
        for spine in ax.spines.values():
            spine.set_linewidth(spec.line_width_axis)

        # Legend if exists
        legend = ax.get_legend()
        if legend:
            for text in legend.get_texts():
                text.set_fontsize(spec.font_legend)


def create_figure(
    nrows: int = 1,
    ncols: int = 1,
    width: str = 'double',
    height_ratio: float = 0.6,
    journal: str = 'default',
    sharex: bool = False,
    sharey: bool = False,
    squeeze: bool = True,
    **kwargs
) -> Tuple[plt.Figure, Union[plt.Axes, List[plt.Axes]]]:
    """
    Create a publication-ready figure with proper sizing.

    Args:
        nrows: Number of subplot rows
        ncols: Number of subplot columns
        width: 'single', '1.5col', or 'double'
        height_ratio: Height relative to width (for single panel)
        journal: Journal name for standards
        sharex: Share x-axis across subplots
        sharey: Share y-axis across subplots
        squeeze: If True, squeeze extra dimensions
        **kwargs: Additional arguments for plt.subplots()

    Returns:
        (fig, axes) tuple

    Example:
        >>> fig, axes = create_figure(1, 3, width='double', journal='nature')
        >>> for ax in axes:
        ...     ax.plot(x, y)
    """
    spec = get_standard(journal)

    # Calculate size
    fig_width = spec.get_width(width)
    panel_height = fig_width * height_ratio / ncols
    fig_height = panel_height * nrows

    # Clamp to max height
    if fig_height > spec.max_height:
        fig_height = spec.max_height

    figsize = (fig_width, fig_height)

    # Create figure
    fig, axes = plt.subplots(
        nrows, ncols,
        figsize=figsize,
        sharex=sharex,
        sharey=sharey,
        squeeze=squeeze,
        **kwargs
    )

    return fig, axes


def get_figure_size(
    width: str = 'double',
    height_ratio: float = 0.6,
    nrows: int = 1,
    ncols: int = 1,
    journal: str = 'default'
) -> Tuple[float, float]:
    """
    Calculate figure size based on journal standards.

    Args:
        width: 'single', '1.5col', or 'double'
        height_ratio: Height relative to width
        nrows, ncols: Subplot grid dimensions
        journal: Journal name

    Returns:
        (width, height) tuple in inches

    Example:
        >>> w, h = get_figure_size('double', journal='nature')
        >>> print(f"{w:.1f} x {h:.1f} inches")
    """
    spec = get_standard(journal)

    fig_width = spec.get_width(width)
    panel_height = fig_width * height_ratio / ncols
    fig_height = min(panel_height * nrows, spec.max_height)

    return (fig_width, fig_height)


# =============================================================================
# QUICK STYLE PRESETS
# =============================================================================

def style_nature():
    """Apply Nature journal style."""
    return set_style('nature')


def style_science():
    """Apply Science journal style."""
    return set_style('science')


def style_cell():
    """Apply Cell journal style."""
    return set_style('cell')


def style_acs():
    """Apply ACS journals style."""
    return set_style('acs')
