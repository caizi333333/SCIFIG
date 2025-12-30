"""
Design Patterns for Scientific Figures
======================================

Implementations of best-practice legend and annotation patterns.

Patterns:
    A - Individual legends (avoid for shared content)
    B - Unified bottom legend (recommended)
    C - Unified right legend
    D - No legend
    E - Title annotation (recommended)
    F - Inline labels (recommended)

Usage:
    >>> from sci_figure_toolkit.patterns import UnifiedLegend, InlineLabel
    >>> UnifiedLegend.apply(fig, axes)
    >>> InlineLabel.add(ax, y=0.9, text='Threshold')
"""

from typing import List, Tuple, Optional, Union, Any
import matplotlib.pyplot as plt
import numpy as np

from .standards import get_standard, FigureSpec


# =============================================================================
# PATTERN B: UNIFIED LEGEND
# =============================================================================

class UnifiedLegend:
    """
    Pattern B: Unified bottom legend for multi-panel figures.

    Use when: All subplots share the same legend items (e.g., frequencies, samples)

    Example:
        >>> fig, axes = plt.subplots(1, 3)
        >>> # ... plot with labels ...
        >>> UnifiedLegend.apply(fig, axes, ncol=3)
    """

    @staticmethod
    def apply(
        fig: plt.Figure,
        axes: Union[plt.Axes, np.ndarray, List[plt.Axes]],
        ncol: int = 3,
        location: str = 'bottom',
        bbox_anchor: Optional[Tuple[float, float]] = None,
        remove_individual: bool = True,
        tight_layout_rect: Optional[List[float]] = None,
        **kwargs
    ) -> None:
        """
        Apply unified legend to figure.

        Args:
            fig: matplotlib Figure
            axes: Axes or array of Axes
            ncol: Number of columns in legend
            location: 'bottom', 'top', or 'right'
            bbox_anchor: Custom anchor point (overrides location default)
            remove_individual: If True, remove individual subplot legends
            tight_layout_rect: Custom rect for tight_layout [left, bottom, right, top]
            **kwargs: Additional arguments for fig.legend()
        """
        # Normalize axes to list
        if hasattr(axes, 'flat'):
            axes_list = list(axes.flat)
        elif isinstance(axes, list):
            axes_list = axes
        else:
            axes_list = [axes]

        # Collect handles and labels
        handles, labels = UnifiedLegend.collect_handles(axes_list)

        if not handles:
            return  # Nothing to do

        # Remove individual legends
        if remove_individual:
            UnifiedLegend.remove_individual(axes_list)

        # Determine anchor and location
        anchor_map = {
            'bottom': (0.5, -0.02),
            'top': (0.5, 1.02),
            'right': (1.02, 0.5),
        }
        loc_map = {
            'bottom': 'lower center',
            'top': 'upper center',
            'right': 'center left',
        }

        anchor = bbox_anchor or anchor_map.get(location, anchor_map['bottom'])
        loc = loc_map.get(location, 'lower center')

        # Create legend
        legend_kwargs = {
            'loc': loc,
            'bbox_to_anchor': anchor,
            'ncol': ncol,
            'frameon': True,
            'fontsize': 8,  # Will be overridden by kwargs if specified
        }
        legend_kwargs.update(kwargs)

        fig.legend(handles, labels, **legend_kwargs)

        # Apply tight layout with proper spacing
        rect = tight_layout_rect
        if rect is None:
            rect_map = {
                'bottom': [0, 0.08, 1, 1],
                'top': [0, 0, 1, 0.92],
                'right': [0, 0, 0.88, 1],
            }
            rect = rect_map.get(location, [0, 0.08, 1, 1])

        fig.tight_layout(rect=rect)

    @staticmethod
    def collect_handles(
        axes: List[plt.Axes],
        deduplicate: bool = True
    ) -> Tuple[List, List[str]]:
        """
        Collect legend handles from all axes.

        Args:
            axes: List of Axes
            deduplicate: If True, remove duplicate labels

        Returns:
            (handles, labels) tuple
        """
        all_handles = []
        all_labels = []

        for ax in axes:
            h, l = ax.get_legend_handles_labels()
            all_handles.extend(h)
            all_labels.extend(l)

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

    @staticmethod
    def remove_individual(axes: List[plt.Axes]) -> None:
        """Remove legend from each individual axes."""
        for ax in axes:
            legend = ax.get_legend()
            if legend is not None:
                legend.remove()


# =============================================================================
# PATTERN E: TITLE ANNOTATION
# =============================================================================

class TitleAnnotation:
    """
    Pattern E: Move annotations into subplot titles.

    Use when:
        - Data fills most of the plot area, leaving no safe position for text
        - Arrow annotations would point at data and occlude it
        - Text boxes or labels would overlap with data curves
        - Need to display key numerical results (optimal values, R², etc.)

    Why this matters:
        - ax.annotate() with arrows often occludes data points
        - Text boxes (bbox=dict(...)) can hide important data curves
        - Title area is always safe and doesn't overlap plot data

    Example:
        >>> # INSTEAD OF: ax.annotate('Peak', xy=(1.5, 1.0), arrowprops=...)
        >>> # USE: Move info to title
        >>> ax.set_title(TitleAnnotation.format(
        ...     "(a) L-curve Analysis",
        ...     optimal_lambda=0.14
        ... ))
    """

    @staticmethod
    def format(
        base_title: str,
        subtitle: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Format title with annotation values.

        Args:
            base_title: Main title text (e.g., "(a) L-curve")
            subtitle: Optional subtitle text
            **kwargs: Key-value pairs to include in subtitle

        Returns:
            Formatted title string

        Example:
            >>> TitleAnnotation.format("(a) Results", R2=0.95, RMSE=0.02)
            '(a) Results\n(R²=0.95, RMSE=0.02)'
        """
        parts = [base_title]

        if kwargs:
            # Format key-value pairs
            formatted = []
            for key, value in kwargs.items():
                # Special formatting for known keys
                if key.lower() in ['r2', 'r_squared']:
                    key_str = 'R²'
                elif key.lower() == 'lambda':
                    key_str = 'λ'
                elif key.lower() == 'beta':
                    key_str = 'β'
                else:
                    key_str = key

                # Format value
                if isinstance(value, float):
                    if abs(value) < 0.01 or abs(value) > 1000:
                        val_str = f"{value:.2e}"
                    else:
                        val_str = f"{value:.3f}"
                else:
                    val_str = str(value)

                formatted.append(f"{key_str}={val_str}")

            subtitle_text = ", ".join(formatted)
            parts.append(f"({subtitle_text})")

        elif subtitle:
            parts.append(f"({subtitle})")

        return "\n".join(parts)

    @staticmethod
    def apply(
        ax: plt.Axes,
        base_title: str,
        fontsize: int = 9,
        **kwargs
    ) -> None:
        """
        Apply formatted title to axes.

        Args:
            ax: matplotlib Axes
            base_title: Main title text
            fontsize: Title font size
            **kwargs: Key-value pairs for subtitle
        """
        title = TitleAnnotation.format(base_title, **kwargs)
        ax.set_title(title, fontsize=fontsize)


# =============================================================================
# PATTERN F: INLINE LABELS
# =============================================================================

class InlineLabel:
    """
    Pattern F: Inline labels on reference lines.

    Use when: Threshold lines, reference lines that would otherwise need legend

    Example:
        >>> ax.axhline(0.9, color='red', linestyle='--')
        >>> InlineLabel.add(ax, y=0.9, text='Threshold', color='red')
    """

    @staticmethod
    def add(
        ax: plt.Axes,
        y: Optional[float] = None,
        x: Optional[float] = None,
        text: str = '',
        position: str = 'right',
        color: str = 'black',
        fontsize: int = 7,
        offset: float = 0.02,
        **kwargs
    ) -> None:
        """
        Add inline label to reference line.

        Args:
            ax: matplotlib Axes
            y: y-coordinate for horizontal line label
            x: x-coordinate for vertical line label
            text: Label text
            position: 'left', 'right', 'top', 'bottom'
            color: Text color
            fontsize: Font size
            offset: Offset from line (in axes fraction)
            **kwargs: Additional text properties
        """
        text_kwargs = {
            'fontsize': fontsize,
            'color': color,
        }
        text_kwargs.update(kwargs)

        if y is not None:
            # Horizontal line label
            if position == 'right':
                ax.text(
                    1 - offset, y, f' {text}',
                    transform=ax.get_yaxis_transform(),
                    ha='right', va='center',
                    **text_kwargs
                )
            else:  # left
                ax.text(
                    offset, y, f'{text} ',
                    transform=ax.get_yaxis_transform(),
                    ha='left', va='center',
                    **text_kwargs
                )

        elif x is not None:
            # Vertical line label
            if position == 'top':
                ax.text(
                    x, 1 - offset, f'{text}',
                    transform=ax.get_xaxis_transform(),
                    ha='center', va='top',
                    rotation=90,
                    **text_kwargs
                )
            else:  # bottom
                ax.text(
                    x, offset, f'{text}',
                    transform=ax.get_xaxis_transform(),
                    ha='center', va='bottom',
                    rotation=90,
                    **text_kwargs
                )

    @staticmethod
    def add_threshold(
        ax: plt.Axes,
        value: float,
        text: str = 'Threshold',
        color: str = 'red',
        linestyle: str = '--',
        linewidth: float = 1.0,
        **kwargs
    ) -> None:
        """
        Add threshold line with inline label (combined convenience method).

        Args:
            ax: matplotlib Axes
            value: Threshold value (y-coordinate)
            text: Label text
            color: Line and text color
            linestyle: Line style
            linewidth: Line width
            **kwargs: Additional arguments for InlineLabel.add()
        """
        ax.axhline(value, color=color, linestyle=linestyle, linewidth=linewidth)
        InlineLabel.add(ax, y=value, text=text, color=color, **kwargs)


# =============================================================================
# BAR CHART UTILITIES
# =============================================================================

def smart_bar_labels(
    ax: plt.Axes,
    bars,
    values: List[float],
    fmt: str = '.3f',
    fontsize: int = 7,
    positive_offset: float = 0.03,
    negative_offset: float = 0.03,
    show_plus: bool = True,
    color: str = 'black'
) -> None:
    """
    Add smart labels to bar chart (handles positive and negative values).

    - Positive values: label above bar
    - Negative values: label below bar

    Args:
        ax: matplotlib Axes
        bars: Bar container from ax.bar()
        values: List of values corresponding to bars
        fmt: Format string for values
        fontsize: Label font size
        positive_offset: Offset above positive bars (in data units)
        negative_offset: Offset below negative bars (in data units)
        show_plus: If True, show '+' sign for positive values
        color: Text color

    Example:
        >>> values = [0.85, -0.12, 0.45]
        >>> bars = ax.bar(['A', 'B', 'C'], values)
        >>> smart_bar_labels(ax, bars, values)
    """
    y_min, y_max = ax.get_ylim()
    y_range = y_max - y_min

    for bar, val in zip(bars, values):
        x = bar.get_x() + bar.get_width() / 2

        if val >= 0:
            y = val + y_range * positive_offset
            va = 'bottom'
            label = f"+{val:{fmt}}" if show_plus else f"{val:{fmt}}"
        else:
            y = val - y_range * negative_offset
            va = 'top'
            label = f"{val:{fmt}}"

        ax.text(x, y, label, ha='center', va=va, fontsize=fontsize, color=color)


def extend_ylim_for_labels(
    ax: plt.Axes,
    values: List[float],
    padding_fraction: float = 0.15
) -> None:
    """
    Extend y-axis limits to accommodate bar labels.

    Args:
        ax: matplotlib Axes
        values: List of bar values
        padding_fraction: Fraction of range to add as padding

    Example:
        >>> values = [0.85, -0.12]
        >>> extend_ylim_for_labels(ax, values)
    """
    current_min, current_max = ax.get_ylim()
    data_min, data_max = min(values), max(values)

    if data_min < 0:
        new_min = data_min * (1 + padding_fraction)
        ax.set_ylim(bottom=min(current_min, new_min))

    if data_max > 0:
        new_max = data_max * (1 + padding_fraction)
        ax.set_ylim(top=max(current_max, new_max))


def bar_labels_inside(
    ax: plt.Axes,
    bars,
    values: List[float],
    stds: Optional[List[float]] = None,
    fmt: str = '.2f',
    fontsize: int = 7,
    color: str = 'white',
    fontweight: str = 'bold',
    min_height_ratio: float = 0.3
) -> None:
    """
    Add labels inside tall bars.

    Args:
        ax: matplotlib Axes
        bars: Bar container
        values: List of values
        stds: Optional list of standard deviations
        fmt: Format string
        fontsize: Font size
        color: Text color (white recommended for colored bars)
        fontweight: Font weight
        min_height_ratio: Minimum bar height (relative to max) to place label inside

    Example:
        >>> bars = ax.bar(x, values)
        >>> bar_labels_inside(ax, bars, values, stds)
    """
    max_height = max(abs(v) for v in values)

    for i, (bar, val) in enumerate(zip(bars, values)):
        # Only place inside if bar is tall enough
        if abs(val) / max_height < min_height_ratio:
            continue

        x = bar.get_x() + bar.get_width() / 2
        y = val / 2  # Middle of bar

        if stds is not None:
            label = f"{val:{fmt}}±{stds[i]:{fmt}}"
        else:
            label = f"{val:{fmt}}"

        ax.text(x, y, label, ha='center', va='center',
                fontsize=fontsize, color=color, fontweight=fontweight)


# =============================================================================
# CONVENIENCE EXPORTS
# =============================================================================

# For backwards compatibility
collect_legend_handles = UnifiedLegend.collect_handles
remove_individual_legends = UnifiedLegend.remove_individual
