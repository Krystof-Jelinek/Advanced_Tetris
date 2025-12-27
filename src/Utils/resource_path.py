"""
This module provides a utility for locating resource files, supporting both standard execution and PyInstaller bundles.
"""
import os
import sys


def resource_path(path: str) -> str:
    """
    Returns the absolute path to a resource file.
    
    Handles the special pathing required when the application is bundled with PyInstaller.
    """
    if hasattr(sys, "_MEIPASS"):
        base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    else:
        base = os.path.abspath(".")

    return os.path.join(base, path)
