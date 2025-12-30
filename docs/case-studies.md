# Case Studies: Real-World Figure Fixes

This document presents real case studies from academic paper figure audits, showing common issues and their solutions.

---

## Case Study 1: Redundant Legends (Figure 3)

### Problem Description

A 3-panel figure showing Double Lorentzian fitting at different frequencies had **identical legends repeated in each subplot**.

```
┌─────────────────┬─────────────────┬─────────────────┐
│ (a) 0.1 Hz      │ (b) 1.0 Hz      │ (c) 10.0 Hz     │
│                 │                 │                 │
│ ● Experimental  │ ● Experimental  │ ● Experimental  │ ← REDUNDANT!
│ — Fit          │ — Fit          │ — Fit          │ ← REDUNDANT!
│                 │                 │                 │
│ [data plot]     │ [data plot]     │ [data plot]     │
└─────────────────┴─────────────────┴─────────────────┘
```

**Issues**:
- Wastes valuable figure space
- Visual clutter distracts from data
- Violates SCI journal guidelines

### Solution: Pattern B - Unified Bottom Legend

```python
from sci_figure_toolkit import UnifiedLegend

# After creating plots with ax.plot(..., label='Experimental')
# Apply Pattern B
UnifiedLegend.apply(fig, axes)
```

**Result**:
```
┌─────────────────┬─────────────────┬─────────────────┐
│ (a) 0.1 Hz      │ (b) 1.0 Hz      │ (c) 10.0 Hz     │
│                 │                 │                 │
│ [data plot]     │ [data plot]     │ [data plot]     │
│                 │                 │                 │
│                 │                 │                 │
└─────────────────┴─────────────────┴─────────────────┘
            ● Experimental  — Double Lorentzian Fit
                     ↑ Single unified legend
```

### Implementation Code

```python
def figure3_fixed(data):
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.5))

    freq_handles, freq_labels = [], []

    for i, (ax, freq) in enumerate(zip(axes, [0.1, 1.0, 10.0])):
        # Plot data
        h1, = ax.plot(T, E_exp, 'o', markersize=4, label='Experimental')
        h2, = ax.plot(T, E_fit, '-', linewidth=1.5, label='Fit')

        # Collect handles from first subplot only
        if i == 0:
            freq_handles = [h1, h2]
            freq_labels = ['Experimental', 'Double Lorentzian Fit']

        ax.set_title(f'({chr(97+i)}) {freq} Hz')
        # NO individual ax.legend() here!

    # Pattern B: Unified bottom legend
    fig.legend(freq_handles, freq_labels,
               loc='lower center',
               bbox_to_anchor=(0.5, -0.02),
               ncol=2, fontsize=8, frameon=True)

    plt.tight_layout(rect=[0, 0.08, 1, 1])  # Leave space for legend
    return fig
```

---

## Case Study 2: Data Occlusion (Figure 4)

### Problem Description

A model comparison figure had a **yellow "Diagnostic only" box that occluded data curves**.

```
┌────────────────────────┐
│ (b) E'' Model          │
│  ┌──────────────────┐  │
│  │ Diagnostic only  │  │ ← Yellow box covering data!
│  └──────────────────┘  │
│      [data curves      │
│       hidden here]     │
└────────────────────────┘
```

**Issues**:
- Critical data invisible
- Misleading visualization
- Poor information hierarchy

### Solution: Pattern E - Title Annotation

Move the diagnostic note to the subplot title:

```python
from sci_figure_toolkit import TitleAnnotation

title = TitleAnnotation.format(
    main_title="(b) E'' Model Comparison",
    note="Diagnostic only, not LOFO-validated"
)
ax.set_title(title, fontsize=9)
```

**Result**:
```
┌────────────────────────────────────┐
│ (b) E'' Model Comparison           │
│ (Diagnostic only, not validated)   │ ← Note in title
│                                    │
│ [all data curves visible]          │
│                                    │
└────────────────────────────────────┘
```

### Implementation Code

```python
def figure4_fixed(data):
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))

    # Subplot (a): E' with LOFO validation
    ax_ep = axes[0]
    ax_ep.plot(T, E_prime_data, 'o', markersize=3)
    ax_ep.plot(T, E_prime_fit, '-', linewidth=1.5)
    ax_ep.set_title("(a) E' Model Comparison\n(LOFO-validated)")

    # Subplot (b): E'' diagnostic only
    ax_epp = axes[1]
    ax_epp.plot(T, E_double_prime_data, 'o', markersize=3)
    ax_epp.plot(T, E_double_prime_fit, '-', linewidth=1.5)

    # Pattern E: Note in title instead of in-figure box
    ax_epp.set_title("(b) E'' Model Comparison\n(Diagnostic only)")

    # Remove any existing text boxes
    # ax_epp.text(...) # REMOVED

    plt.tight_layout()
    return fig
```

---

## Case Study 3: Broken Annotations (Figure 6)

### Problem Description

An L-curve analysis figure had a **broken annotation showing ".0e"** instead of the full scientific notation.

```
┌────────────────────────┐
│ (a) L-curve            │
│                        │
│        ●               │
│       / \              │
│      /   \     .0e     │ ← Broken format string!
│     ●     ●            │
│                        │
└────────────────────────┘
```

**Issues**:
- Unprofessional appearance
- Missing critical information (optimal λ value)
- Code bug visible in output

### Solution: Pattern E - Move to Title

```python
# Instead of broken annotation
# ax.annotate('.0e', ...)  # BUG!

# Move to title with proper formatting
ax.set_title(f'(a) L-curve Analysis\n(Optimal λ = {opt_lambda:.2e})')
```

**Result**:
```
┌────────────────────────────────────┐
│ (a) L-curve Analysis               │
│ (Optimal λ = 1.40e-01)             │ ← Clean, readable
│                                    │
│        ●                           │
│       / \                          │
│      /   \                         │
│     ●     ●                        │
└────────────────────────────────────┘
```

---

## Case Study 4: Reference Line Occlusion (Figure 8)

### Problem Description

A residual analysis figure had **"±3× pooled SD" text occluding residual data points**.

```
┌────────────────────────────────────┐
│ ±3× pooled SD                      │ ← Text covering data!
│ ─────────────────── (upper bound)  │
│  ● ●  ●   ●  ● ●  ●               │
│ ─────────────────── (lower bound)  │
│                                    │
│ ● 0.1 Hz  ● 1.0 Hz  ● 10.0 Hz     │ ← Redundant legend
└────────────────────────────────────┘
```

**Issues**:
- Text covers important residual data
- Redundant legends in multi-panel figure
- Reference line meaning unclear

### Solution: Pattern B + Pattern F Combined

```python
from sci_figure_toolkit import UnifiedLegend, InlineLabel

# Pattern F: Inline label on reference line
std = np.std(residuals)
ax.axhline(3*std, color='red', linestyle='--', linewidth=0.8)
ax.axhline(-3*std, color='red', linestyle='--', linewidth=0.8)

InlineLabel.add(ax, y=3*std, label=r'$\pm 3\sigma$', position='right')

# Pattern B: Unified legend for frequencies
UnifiedLegend.apply(fig, axes)
```

**Result**:
```
┌────────────────────────────────────┐
│ ─────────────────────────── ±3σ    │ ← Inline label
│  ● ●  ●   ●  ● ●  ●               │
│ ───────────────────────────        │
│                                    │
└────────────────────────────────────┘
        ● 0.1 Hz  ● 1.0 Hz  ● 10.0 Hz
                ↑ Unified legend
```

### Implementation Code

```python
def figure8_fixed(residual_data):
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.8))

    freq_handles, freq_labels = [], []

    for i, (ax, freq) in enumerate(zip(axes, [0.1, 1.0, 10.0])):
        residuals = residual_data[freq]
        std_resid = np.std(residuals)

        # Plot residuals
        h, = ax.scatter(T, residuals, s=16, alpha=0.7, label=f'{freq} Hz')

        if i == 0:
            freq_handles.append(h)
            freq_labels.append(f'{freq} Hz')

        # Reference lines with Pattern F inline labels
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axhline(3*std_resid, color='red', linestyle='--', linewidth=0.8)
        ax.axhline(-3*std_resid, color='red', linestyle='--', linewidth=0.8)

        # Pattern F: Inline label (only on last subplot to avoid clutter)
        if i == len(axes) - 1:
            ax.text(0.98, 3*std_resid, r'$\pm 3\sigma$',
                    transform=ax.get_yaxis_transform(),
                    fontsize=7, color='red', ha='right', va='bottom')

    # Pattern B: Unified bottom legend
    fig.legend(freq_handles, freq_labels,
               loc='lower center',
               bbox_to_anchor=(0.35, -0.02),
               ncol=3, fontsize=8, frameon=True)

    plt.tight_layout(rect=[0, 0.08, 1, 1])
    return fig
```

---

## Case Study 5: Bar Chart Label Placement (Figure 19)

### Problem Description

A feature importance bar chart had **negative value labels inside short bars with white text**, making them invisible.

```
┌────────────────────────────────────┐
│ Feature Importance                 │
│                                    │
│ ██████████████████ 0.95            │
│ ████████████████ 0.82              │
│ ██████████████ 0.76                │
│ █ [invisible]                      │ ← White "-0.096" on short bar!
│ ████████████ 0.65                  │
└────────────────────────────────────┘
```

**Issues**:
- Negative value label completely invisible
- White text on short colored bar
- Inconsistent label placement logic

### Solution: Smart Bar Labels

```python
from sci_figure_toolkit import smart_bar_labels

bars = ax.bar(x, values)
smart_bar_labels(ax, bars, values)
```

**Result**:
```
┌────────────────────────────────────┐
│ Feature Importance                 │
│                                    │
│ ██████████████████ 0.95            │
│ ████████████████ 0.82              │
│ ██████████████ 0.76                │
│ █                                  │
│ -0.096                             │ ← Black text below bar
│ ████████████ 0.65                  │
└────────────────────────────────────┘
```

### Implementation Code

```python
from sci_figure_toolkit.patterns import smart_bar_labels

def figure19_fixed(feature_data):
    fig, ax = plt.subplots(figsize=(7.0, 4.0))

    features = list(feature_data.keys())
    values = list(feature_data.values())

    # Create bar chart
    colors = ['#D55E00' if v < 0 else '#0072B2' for v in values]
    bars = ax.barh(features, values, color=colors)

    # Smart label placement
    smart_bar_labels(ax, bars, values, orientation='horizontal')

    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_xlabel('Importance Score')
    ax.set_xlim(-0.25, 1.05)  # Extended to fit labels

    plt.tight_layout()
    return fig
```

---

## Audit Workflow Summary

### Before Submission Checklist

```python
from sci_figure_toolkit import FigureAuditor

# 1. Create your figure
fig, axes = create_my_figure(data)

# 2. Run audit
auditor = FigureAuditor(journal='nature')
issues = auditor.audit_figure(fig, list(axes.flat))

# 3. Review issues
auditor.print_report()

# 4. Apply fixes based on issue types
for issue in issues:
    if issue.type == IssueType.REDUNDANT_LEGEND:
        # Apply Pattern B
        UnifiedLegend.apply(fig, axes)
    elif issue.type == IssueType.DATA_OCCLUSION:
        # Apply Pattern E or F
        pass
    # ... handle other issue types

# 5. Re-audit until clean
issues = auditor.audit_figure(fig, list(axes.flat))
assert len(issues) == 0, "Still have issues to fix!"

# 6. Save in publication formats
save_figure(fig, 'output/Figure1', formats=['pdf', 'png', 'svg'])
```

---

## Pattern Quick Reference

| Pattern | Problem | Solution | Code |
|---------|---------|----------|------|
| **B** | Redundant legends | Unified bottom legend | `UnifiedLegend.apply(fig, axes)` |
| **E** | In-figure annotations | Move to title | `TitleAnnotation.format(...)` |
| **F** | Reference line labels | Inline labels | `InlineLabel.add(ax, y, label)` |
| **Smart Labels** | Bar label placement | Intelligent positioning | `smart_bar_labels(ax, bars, vals)` |
