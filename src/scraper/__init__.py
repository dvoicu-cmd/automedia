"""
package __init__: scraper
"""

from .platform_strategies import *
from .platform_strategies import __all__ as scraper_platform_strategies_all

from .downloader import DownloadManager

__all__ = scraper_platform_strategies_all + ['DownloadManager']
