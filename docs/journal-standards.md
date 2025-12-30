# Journal Standards Reference

Complete reference for figure specifications across major scientific journals.

---

## Quick Reference Table

| Journal | Single Column | Double Column | Min DPI | Font Range |
|---------|--------------|---------------|---------|------------|
| **Nature** | 3.5" (89mm) | 7.0" (178mm) | 300 | 5-7pt |
| **Science** | 2.25" (57mm) | 6.0" (152mm) | 300 | 6-8pt |
| **Cell** | 3.35" (85mm) | 6.85" (174mm) | 300 | 6-8pt |
| **ACS** | 3.25" (83mm) | 7.0" (178mm) | 300 | 6-8pt |
| **RSC** | 3.25" (83mm) | 6.75" (171mm) | 600 | 7-8pt |
| **Elsevier** | 3.5" (90mm) | 7.0" (190mm) | 300 | 6-8pt |
| **Wiley** | 3.4" (86mm) | 7.0" (178mm) | 300 | 6-8pt |
| **IEEE** | 3.5" (88mm) | 7.16" (182mm) | 300 | 8-10pt |
| **PNAS** | 3.42" (87mm) | 7.0" (178mm) | 300 | 6-8pt |
| **PLOS** | 3.27" (83mm) | 6.83" (173mm) | 300 | 8-12pt |

---

## Detailed Journal Specifications

### Nature Publishing Group

**Journals**: Nature, Nature Communications, Nature Methods, etc.

```python
from sci_figure_toolkit import get_standard, JournalStandard

nature = get_standard(JournalStandard.NATURE)
```

| Parameter | Value | Notes |
|-----------|-------|-------|
| Single column | 3.5" (89mm) | Standard figure width |
| 1.5 column | 5.5" (140mm) | Medium-width figure |
| Double column | 7.0" (178mm) | Full-width figure |
| Maximum height | 9.0" (228mm) | Page constraint |
| **Font size** | 5-7pt | Minimum 5pt for readability |
| Line width | 0.5-1pt | For axes and data lines |
| DPI | 300 (min) | 600 recommended for print |
| Color mode | CMYK | For print; RGB for online |

**Special Requirements**:
- Arial or Helvetica fonts preferred
- Scale bars required for microscopy images
- Statistical annotations (*, **, ***) with p-value definitions

---

### Science (AAAS)

**Journals**: Science, Science Advances, Science Signaling

```python
science = get_standard(JournalStandard.SCIENCE)
```

| Parameter | Value | Notes |
|-----------|-------|-------|
| Single column | 2.25" (57mm) | Narrow format |
| 1.5 column | 4.5" (114mm) | Medium width |
| Double column | 6.0" (152mm) | Full width (narrower than Nature) |
| Maximum height | 9.0" (228mm) | |
| **Font size** | 6-8pt | Helvetica preferred |
| Line width | 0.5-1pt | |
| DPI | 300 (min) | |

**Special Requirements**:
- Helvetica or Arial fonts only
- Figure legends must be separate from figures
- Color figures may have additional fees

---

### Cell Press

**Journals**: Cell, Cell Reports, Molecular Cell, etc.

```python
cell = get_standard(JournalStandard.CELL)
```

| Parameter | Value | Notes |
|-----------|-------|-------|
| Single column | 3.35" (85mm) | |
| 1.5 column | 5.08" (129mm) | |
| Double column | 6.85" (174mm) | |
| Maximum height | 9.0" (228mm) | |
| **Font size** | 6-8pt | |
| Line width | 0.5-1pt | |
| DPI | 300 (min) | |

**Special Requirements**:
- Arial font required
- STAR Methods formatting for methods figures
- Graphical abstracts: 16:9 aspect ratio

---

### ACS Publications

**Journals**: JACS, ACS Nano, Chemistry of Materials, etc.

```python
acs = get_standard(JournalStandard.ACS)
```

| Parameter | Value | Notes |
|-----------|-------|-------|
| Single column | 3.25" (83mm) | |
| Double column | 7.0" (178mm) | |
| Maximum height | 9.5" (241mm) | |
| **Font size** | 6-8pt | |
| Line width | 0.5-1.5pt | |
| DPI | 300 (min) | 600 for TOC graphics |

**Special Requirements**:
- Helvetica, Arial, or Times New Roman
- TOC/Abstract graphics: 1.375" × 3.25" or 2" × 4.75"
- Scheme and Chart numbering required

---

### RSC Publications

**Journals**: Chem. Commun., J. Mater. Chem., RSC Advances, etc.

```python
rsc = get_standard(JournalStandard.RSC)
```

| Parameter | Value | Notes |
|-----------|-------|-------|
| Single column | 3.25" (83mm) | |
| Double column | 6.75" (171mm) | |
| Maximum height | 9.5" (241mm) | |
| **Font size** | 7-8pt | |
| Line width | 0.5-1pt | |
| DPI | 600 (min) | Higher than most journals |

**Special Requirements**:
- Sans-serif fonts preferred
- ChemDraw structures at specific bond lengths
- ESI figures can have different specifications

---

### Elsevier Journals

**Journals**: Various (check specific journal guidelines)

```python
elsevier = get_standard(JournalStandard.ELSEVIER)
```

| Parameter | Value | Notes |
|-----------|-------|-------|
| Single column | 3.5" (90mm) | Varies by journal |
| 1.5 column | 5.5" (140mm) | |
| Double column | 7.0" (190mm) | |
| **Font size** | 6-8pt | |
| Line width | 0.5-1pt | |
| DPI | 300 (min) | |

**Special Requirements**:
- Varies significantly by journal
- Always check specific journal guidelines
- Graphical abstract dimensions vary

---

### Wiley Journals

**Journals**: Angewandte Chemie, Advanced Materials, etc.

```python
wiley = get_standard(JournalStandard.WILEY)
```

| Parameter | Value | Notes |
|-----------|-------|-------|
| Single column | 3.4" (86mm) | |
| Double column | 7.0" (178mm) | |
| Maximum height | 9.5" (241mm) | |
| **Font size** | 6-8pt | |
| Line width | 0.5-1pt | |
| DPI | 300 (min) | |

**Special Requirements**:
- Helvetica or Arial preferred
- TOC graphics with specific dimensions
- Supporting Information has relaxed requirements

---

### IEEE Publications

**Journals**: IEEE Trans., IEEE Access, etc.

```python
ieee = get_standard(JournalStandard.IEEE)
```

| Parameter | Value | Notes |
|-----------|-------|-------|
| Single column | 3.5" (88mm) | |
| Double column | 7.16" (182mm) | Two-column format |
| **Font size** | 8-10pt | Larger than other publishers |
| Line width | 0.5-1pt | |
| DPI | 300 (min) | |

**Special Requirements**:
- Times New Roman for text elements
- Figure captions below figures
- Tables caption above tables
- Specific requirements for conference papers vs journals

---

## Font Specifications

### Recommended Fonts by Publisher

| Publisher | Primary Font | Alternatives |
|-----------|-------------|--------------|
| Nature | Helvetica | Arial |
| Science | Helvetica | Arial |
| Cell | Arial | Helvetica |
| ACS | Helvetica | Arial, Times |
| RSC | Sans-serif | Helvetica, Arial |
| Elsevier | Varies | Check journal |
| Wiley | Helvetica | Arial |
| IEEE | Times New Roman | Arial |

### Font Size Guidelines

```python
# Recommended font sizes for publication
FONT_SIZES = {
    'axis_label': 9,      # Axis labels (x, y titles)
    'tick_label': 8,      # Tick mark labels
    'title': 9,           # Figure title
    'legend': 8,          # Legend text
    'annotation': 7,      # In-figure annotations
    'panel_label': 9,     # (a), (b), (c) labels
}
```

**Important**: After reduction to publication size, fonts must remain readable. A 9pt font in a double-column figure may appear as 4.5pt when printed in single-column.

---

## Color Specifications

### Colorblind-Safe Palette

Based on Wong, B. (2011) Nature Methods recommendations:

```python
from sci_figure_toolkit import colorblind_palette

colors = colorblind_palette(n=8)
# Returns: ['#0072B2', '#D55E00', '#009E73', '#CC79A7',
#           '#F0E442', '#56B4E9', '#E69F00', '#000000']
```

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| Blue | #0072B2 | (0, 114, 178) | Primary data |
| Vermillion | #D55E00 | (213, 94, 0) | Emphasis/contrast |
| Bluish green | #009E73 | (0, 158, 115) | Secondary data |
| Reddish purple | #CC79A7 | (204, 121, 167) | Categorical |
| Yellow | #F0E442 | (240, 228, 66) | Highlights |
| Sky blue | #56B4E9 | (86, 180, 233) | Background |
| Orange | #E69F00 | (230, 159, 0) | Warnings |
| Black | #000000 | (0, 0, 0) | Text/lines |

### Color Mode Requirements

| Purpose | Color Mode | Notes |
|---------|------------|-------|
| Print | CMYK | Required for physical journals |
| Online | RGB | Web and PDF viewing |
| Grayscale | Grayscale | Some journals require grayscale-compatible figures |

---

## Line and Marker Specifications

### Line Widths

```python
LINE_WIDTHS = {
    'data': 1.5,          # Data lines
    'fit': 1.5,           # Fitted curves
    'reference': 1.0,     # Reference/threshold lines
    'axis': 0.8,          # Axis spines
    'grid': 0.5,          # Grid lines (if used)
}
```

### Marker Sizes

```python
MARKER_SIZES = {
    'data': 4,            # Data points
    'highlight': 6,       # Emphasized points
    'small': 3,           # Dense data
}
```

---

## File Format Requirements

### Vector Formats (Preferred)

| Format | Best For | Notes |
|--------|----------|-------|
| PDF | Final submission | Preserves vector quality |
| EPS | Legacy systems | Some journals still require |
| SVG | Web/online | Editable in vector editors |

### Raster Formats

| Format | DPI | Best For | Notes |
|--------|-----|----------|-------|
| TIFF | 600+ | Photos, microscopy | Uncompressed, large files |
| PNG | 600+ | Graphs with text | Lossless compression |
| JPEG | 300+ | Photographs only | Lossy, avoid for graphs |

### Recommended Export Settings

```python
from sci_figure_toolkit import save_figure

# Save in multiple formats
save_figure(fig, 'output/figure1',
            formats=['pdf', 'png', 'svg'],
            dpi=600,
            transparent=False)
```

---

## Common Issues and Solutions

### Issue 1: Font Size Too Small After Reduction

**Problem**: Fonts appear unreadable when figure is reduced to column width.

**Solution**:
```python
# Calculate effective font size
original_width = 10.0  # inches (working size)
final_width = 3.5      # inches (publication size)
scale = final_width / original_width  # 0.35

working_fontsize = 9 / scale  # ≈ 26pt in working figure
# This will become 9pt in final publication
```

### Issue 2: Line Weights Too Thin

**Problem**: Lines disappear or become invisible in print.

**Solution**: Minimum 0.5pt lines; test by printing at actual size.

### Issue 3: Colors Not Distinguishable

**Problem**: Colorblind readers cannot distinguish data series.

**Solution**:
- Use colorblind-safe palette
- Add patterns/markers in addition to colors
- Test with colorblind simulation tools

---

## Toolkit Usage for Journal Compliance

```python
from sci_figure_toolkit import (
    set_style, create_figure, FigureAuditor,
    get_standard, JournalStandard
)

# 1. Set journal-specific style
set_style(JournalStandard.NATURE)

# 2. Create compliant figure
fig, axes = create_figure(nrows=1, ncols=3, width='double')

# 3. Create your plots
# ... plotting code ...

# 4. Audit before submission
auditor = FigureAuditor(journal='nature')
issues = auditor.audit_figure(fig, axes)
auditor.print_report()

# 5. Fix issues and re-audit until clean
```

---

## References

1. Nature Author Guidelines: https://www.nature.com/nature/for-authors
2. Science Author Guidelines: https://www.science.org/content/page/instructions-preparing-initial-manuscript
3. Cell Press Figure Guidelines: https://www.cell.com/figure-guidelines
4. ACS Graphics Guidelines: https://pubs.acs.org/page/4authors/graphics
5. RSC Author Guidelines: https://www.rsc.org/journals-books-databases/author-and-reviewer-hub/
6. Wong, B. (2011). Color blindness. Nature Methods, 8(6), 441.
