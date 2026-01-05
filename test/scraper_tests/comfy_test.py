from context import src

import json
import urllib
import uuid
import websocket
from urllib import request, parse
import time

import random
from src.scraper.platform_strategies.comfy_ui_api import ComfyUiAPI

comfy = ComfyUiAPI("ollama-host")
comfy.set_prompt(1920, 1080, 1, "elizabeth warren calling george w bush because she is upset that the Pentagon is getting audited,but she is looking at the world trade center along with osama binladen is watching them from heaven. Draw your prompt in the style of a charlie hebdo cartoon.")
comfy.stable_diffusion()


