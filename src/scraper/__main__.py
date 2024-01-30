from context import src
from context import lib

from src.scraper.platform_strategies import *


if __name__ == '__main__':
    ai = OpenAiAPI()
    print(ai.text_llm(model='gpt-3.5-turbo',
                      system_msg='You are an ai from openAI',
                      user_msg='Is it okay to shit the bed? Just give me a yes or no response',
                      to_file=False)
          )


