#!/usr/bin/env python3
"""
Command-line interface for sci-figure-toolkit.

Usage:
    sci-figure-audit <file.py>           Audit Python source file
    sci-figure-audit --journal nature    Set target journal
    sci-figure-audit --list-journals     List available journals
"""

import argparse
import sys
from pathlib import Path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='sci-figure-audit',
        description='Audit Python figure code for SCI publication compliance',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    sci-figure-audit my_plots.py
    sci-figure-audit my_plots.py --journal nature
    sci-figure-audit --list-journals

For more information, visit:
    https://github.com/sci-figure/sci-figure-toolkit
'''
    )

    parser.add_argument(
        'file',
        nargs='?',
        help='Python file to audit'
    )

    parser.add_argument(
        '--journal', '-j',
        default='nature',
        help='Target journal standard (default: nature)'
    )

    parser.add_argument(
        '--list-journals',
        action='store_true',
        help='List available journal standards'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output with fix suggestions'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # Handle --list-journals
    if args.list_journals:
        from .standards import list_journals
        print("\nAvailable Journal Standards:")
        print("-" * 30)
        for journal in list_journals():
            print(f"  - {journal}")
        print("\nUsage: sci-figure-audit file.py --journal <name>\n")
        return 0

    # Require file argument if not listing journals
    if not args.file:
        parser.print_help()
        return 1

    # Check file exists
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        return 1

    if not filepath.suffix == '.py':
        print(f"Warning: Expected .py file, got {filepath.suffix}", file=sys.stderr)

    # Run audit
    try:
        from .auditor import CodeAuditor

        print(f"\n{'=' * 60}")
        print(f"SCI Figure Audit Report")
        print(f"{'=' * 60}")
        print(f"File:    {filepath}")
        print(f"Journal: {args.journal}")
        print(f"{'=' * 60}\n")

        auditor = CodeAuditor(journal=args.journal)
        issues = auditor.audit_file(str(filepath))

        if not issues:
            print("✅ No issues found! Code appears publication-ready.\n")
            return 0

        # Group issues by severity
        errors = [i for i in issues if i.severity.name == 'ERROR']
        warnings = [i for i in issues if i.severity.name == 'WARNING']
        info = [i for i in issues if i.severity.name == 'INFO']

        if errors:
            print(f"🔴 ERRORS ({len(errors)}):")
            for issue in errors:
                print(f"   [{issue.type.name}] {issue.message}")
                if issue.location:
                    print(f"      Location: {issue.location}")
                if args.verbose and issue.suggestion:
                    print(f"      Fix: {issue.suggestion}")
            print()

        if warnings:
            print(f"🟡 WARNINGS ({len(warnings)}):")
            for issue in warnings:
                print(f"   [{issue.type.name}] {issue.message}")
                if issue.location:
                    print(f"      Location: {issue.location}")
                if args.verbose and issue.suggestion:
                    print(f"      Fix: {issue.suggestion}")
            print()

        if info:
            print(f"🔵 INFO ({len(info)}):")
            for issue in info:
                print(f"   [{issue.type.name}] {issue.message}")
            print()

        # Summary
        print(f"{'=' * 60}")
        print(f"Summary: {len(errors)} errors, {len(warnings)} warnings, {len(info)} info")
        print(f"{'=' * 60}\n")

        # Return error code if there are errors
        return 1 if errors else 0

    except ImportError as e:
        print(f"Error: Missing dependency: {e}", file=sys.stderr)
        print("Install with: pip install sci-figure-toolkit", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
