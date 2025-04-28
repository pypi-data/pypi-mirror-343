"""
Robot Framework DomRetryLibrary
===================================

A Robot Framework library with AI-powered fallback for locator variables,
enhancing test reliability by using OpenAI to dynamically generate element
locators when primary locators fail.
"""

from .core import DomRetryLibrary

__version__ = "1.0.0"
__author__ = "Kristijan Plaushku"
__email__ = "info@plaushkusolutions.com"
__license__ = "MIT"

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