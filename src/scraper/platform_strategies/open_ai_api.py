from openai import OpenAI
from dotenv import load_dotenv
import os
from src.scraper.downloader import DownloadManager


class OpenAiAPI:
    def __init__(self):
        load_dotenv()
        key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=key)
        self.dm = DownloadManager()

    def text_llm(self, model, system_msg, user_msg, to_file=True):
        """
        Text generation from openAI
        https://platform.openai.com/docs/guides/text-generation
        :param model: gpt-4, gpt-4 turbo, gpt-3.5-turbo
        :param system_msg: The string input that describes how the model should act
        :param user_msg: The message sent to the model
        :param max_tokens: The maximum number of tokens to use.
        :param to_file: Boolean value determining to out put to a string or to a file
        :return: The message in a text file
        """

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
        )
        str_response = response.choices[0].message.content
        if to_file:
            self.dm.dl_text(str_response, f"llm_txt_{user_msg[:10]}")
            return None
        else:
            return str_response

    def stable_diffusion(self, prompt):
        """
        Creates a 1024x1024 image and downloads it
        https://platform.openai.com/docs/guides/images?context=node
        :param prompt: The string input describing the image to generate
        :return: Downloads a file in
        """
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        self.dm.dl_via_link(image_url, "image", f"sd_{prompt[:10]}")

    def text_to_speech(self, voice, str_input):
        """
        The text to speach models from openAI
        https://platform.openai.com/docs/guides/text-to-speech

        :param voice: alloy, echo, fable, onyx, nova, and shimmer
        :param str_input: text to input
        """
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=str_input
        )

        wd = f"{self.dm.dl_root()}/audio"
        response.stream_to_file(f"{wd}/{self.dm.get_rand_id()}_tts_{str_input[:10]}.mp3")
