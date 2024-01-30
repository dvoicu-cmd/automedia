"""
package __init__: scraper.platform_strategies
"""

# Exporting classes
from .open_ai_api import OpenAiAPI
from .pyttsx3_wraper import TTS
from .reddit_web import RedditScrape

__all__ = ['OpenAiAPI', 'TTS', 'RedditScrape']
