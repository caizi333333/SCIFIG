# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12

### Added

#### Core Features
- **FigureAuditor**: Automated figure quality checking
  - Redundant legend detection across subplots
  - Data occlusion detection (legend/annotation blocking data)
  - Font consistency validation
  - Figure size standards compliance
  - Colorblind accessibility checking

- **CodeAuditor**: Python source code analysis
  - Pattern detection for common figure issues
  - Auto-fix suggestions with code snippets
  - Support for `.py` file scanning

#### Design Patterns
- **Pattern B**: Unified bottom legend for multi-panel figures
- **Pattern E**: Title annotations for key values
- **Pattern F**: Inline labels for reference lines
- **Smart Bar Labels**: Intelligent label placement for positive/negative values

#### Journal Standards
- Pre-configured standards for 10+ major journals:
  - Nature Publishing Group
  - Science (AAAS)
  - Cell Press
  - ACS Publications
  - RSC Publications
  - Elsevier journals
  - Wiley journals
  - IEEE publications
  - PNAS
  - PLOS ONE

#### Utilities
- `save_figure()`: Multi-format export (PDF, PNG, SVG, TIFF)
- `collect_legend_handles()`: Legend aggregation from multiple axes
- `colorblind_palette()`: Wong 2011 colorblind-safe colors
- Unit conversion helpers (mm, cm, inches)

### Documentation
- Comprehensive README with quick start guide
- Journal standards reference documentation
- Case studies with before/after examples
- API documentation for all public functions

## [0.9.0] - 2024-12 (Pre-release)

### Added
- Initial implementation based on DMA_Modeling_System figure audit
- Core auditing functionality
- Basic pattern implementations

---

## Planned Features

### [1.1.0] - Future
- [ ] Interactive web-based audit dashboard
- [ ] LaTeX figure integration
- [ ] Batch processing CLI
- [ ] More journal presets (Springer, Taylor & Francis)
- [ ] PDF figure extraction and analysis

### [1.2.0] - Future
- [ ] AI-powered layout suggestions
- [ ] Automatic fix application
- [ ] Figure template gallery
- [ ] Integration with Overleaf
