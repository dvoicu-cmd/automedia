from src.scraper.platform_strategies.open_ai_api import OpenAiAPI

def speech():
    ai = OpenAiAPI()
    ai.text_to_speech("echo", "Man, I remember having sex with a bath bomb in a bath and body works one time. Good shit.")

def image():
    ai = OpenAiAPI()
    ai.stable_diffusion("A Bath&BodyWorks candle holding a minecraft sword sword diamond sword")

def text():
    ai = OpenAiAPI()
    res = ai.text_llm("gpt-4", "You are gpt-4-turbo", "Tell me a the story about how you were made.", 80)
    print(res)


speech()
image()
text()
