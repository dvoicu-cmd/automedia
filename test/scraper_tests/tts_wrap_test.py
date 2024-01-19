from context import src
from src.scraper.platform_strategies.pyttsx3_wraper import TTS

tts = TTS(125,0.5,'g')
tts.dl_text('Sample text, bottom text. Real shit right here am I right?', 'real')

