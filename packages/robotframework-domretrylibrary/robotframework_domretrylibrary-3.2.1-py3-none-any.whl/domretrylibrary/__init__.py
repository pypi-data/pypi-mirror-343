"""
Robot Framework DomRetryLibrary
===================================

A Robot Framework library with AI-powered fallback for locator variables,
enhancing test reliability by using OpenAI to dynamically generate element
locators when primary locators fail.
"""

# Import the main class
from .core import DomRetryLibrary

# Version information
__version__ = "3.2.1"
__author__ = "Kristijan Plaushku"
__email__ = "info@plaushkusolutions.com"
__license__ = "MIT"

# Explicitly define what gets imported with "from domretrylibrary import *"
__all__ = ["DomRetryLibrary"]

def get_library_instance():
    """
    Get a new instance of the DomRetryLibrary.
    
    Returns:
        DomRetryLibrary: A new instance of the DomRetryLibrary.
    """
    try:
        return DomRetryLibrary()
    except Exception as e:
        import sys
        sys.stderr.write(f"Error creating DomRetryLibrary instance: {e}\n")
        raise