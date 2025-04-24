"""
Robot Framework AI DomRetryLibrary
==================================

A Robot Framework library with AI-powered fallback for locator variables,
enhancing test reliability by using OpenAI to dynamically generate element
locators when primary locators fail.

For more information and usage examples, see:
https://github.com/plaushku/robot-dom-retry-library
"""

# Direct import to make the class available at the top level
from dom_retry_library import DomRetryLibrary

# Make the class directly importable from the package
DomRetryLibrary = DomRetryLibrary

__version__ = "0.1.3" 