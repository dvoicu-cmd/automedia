from openai import OpenAI
from dotenv import load_dotenv
import os

from lib.manage_directory_structure.scraper_dir_manager import ScraperDirManager


class OpenAiAPI:
    """
    Wrapper class that encapsulates the OpenAI api python library into a simple class.
    """
    def __init__(self):
        load_dotenv()
        key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=key)
        self.dm = ScraperDirManager()

    def text_llm(self, model, system_msg, user_msg, to_file=True, path_dir_output=''):
        """
        Text generation from openAI
        https://platform.openai.com/docs/guides/text-generation
        :param model: gpt-4, gpt-4 turbo, gpt-3.5-turbo
        :param system_msg: The string input that describes how the model should act
        :param user_msg: The message sent to the model
        :param path_dir_output: The absolute path of the output directory
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
            self.dm.dl_text(str_response, f"llm_txt_{user_msg[:10]}", path_dir_output)
            return None
        else:
            return str_response

    def stable_diffusion(self, prompt, path_dir_output=''):
        """
        Creates a 1024x1024 image and downloads it
        https://platform.openai.com/docs/guides/images?context=node
        :param prompt: The string input describing the image to generate
        :param path_dir_output The absolute path of the output directory
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
        self.dm.dl_via_link(image_url, "image", f"sd_{prompt[:10]}", path_dir_output)

    def text_to_speech(self, voice, str_input, path_dir_output=''):
        """
        The text to speach models from openAI
        https://platform.openai.com/docs/guides/text-to-speech

        :param voice: alloy, echo, fable, onyx, nova, and shimmer
        :param path_dir_output The absolute path of the output directory
        :param str_input: text to input
        """
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=str_input
        )
        response.stream_to_file(f"{path_dir_output}/{self.dm.get_rand_id()}_tts_{str_input[:10]}.mp3")
