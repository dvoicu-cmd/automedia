from context import src
from src.scraper.platform_strategies.ollama_api import OllamaAPI

ai = OllamaAPI("ollama-host")
res = ai.text_llm("dolphin2.9.3", "text", "text", False, path_dir_output="/")
print(res)
