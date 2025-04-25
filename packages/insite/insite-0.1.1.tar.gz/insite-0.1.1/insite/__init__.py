"""
InSite - A tool for crawling websites and compiling PDFs of their pages.

This module is primarily intended for crawling code documentation websites
to download PDFs for offline knowledge supplementation and RAG implementations in LLMs.
"""

__version__ = "0.1.1"

from .scraper import InsiteScraper
from .processor import InsiteProcessor

__all__ = ['InsiteScraper', 'InsiteProcessor']
