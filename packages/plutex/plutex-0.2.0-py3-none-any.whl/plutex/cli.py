#!/usr/bin/env python3
"""
CLI entry point for plutex
"""
import sys
from plutex.main import main as _main_function

def main() -> int:
    """
    Main entry point for the command-line interface.
    
    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    return _main_function()

if __name__ == "__main__":
    sys.exit(main())