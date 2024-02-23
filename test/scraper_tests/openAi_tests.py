from context import src
from src.scraper.platform_strategies.open_ai_api import OpenAiAPI

def speech():
    ai = OpenAiAPI()
    ai.text_to_speech("echo", "Man, I remember having sex with a bath bomb in a bath and body works one time. Good shit.")

def image():
    ai = OpenAiAPI()
    ai.stable_diffusion("I want you to generate me an image of a goofy cartoony looney tunes looking ahh nerd with giant glasses reading with intense focus at a comically large book. He also is holding a comically large spoon while smerking at the book.", '/Users/dvoicu/mnt/GoofyTestFiles/minecraft parkour')

def text():
    ai = OpenAiAPI()
    res = ai.text_llm("gpt-4", "You are gpt-4-turbo", "Tell me a the story about how you were made.", 80)
    print(res)


image()

