from openai import OpenAI
from dotenv import load_dotenv
import os
import random
import requests


class OpenAiAPI:
    def __init__(self):
        load_dotenv()
        key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=key)
        self.rand = random.randint(10000, 99999)
        return

    def text_llm(self, model, system_msg, user_msg, max_tokens=4096):

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=max_tokens
        )
        print(response)

        str_response = response.choices[0].message.content

        print(str_response)

        self.__mkdir("openai_text")
        wd = os.getcwd()

        with open(f"{wd}/openai_text/{self.rand}_llm_txt_{user_msg[:10]}.txt", "w") as f:
            f.write(str_response)


    def stable_diffusion(self, prompt):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        self.__mkdir("openai_image")
        wd = os.getcwd()

        image_url = response.data[0].url
        img_request = requests.get(image_url)

        if img_request.status_code == 200:
            with open(f"{wd}/openai_image/{self.rand}_sd_{prompt[:10]}.jpg", "wb") as f:
                f.write(img_request.content)
        else:
            raise ProcessLookupError(f"Failed to read image at link:{image_url}")

    def text_to_speech(self, voice, str_input):
        """

        https://platform.openai.com/docs/guides/text-to-speech
        """
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=str_input
        )

        self.__mkdir("openai_speech")
        wd = os.getcwd()

        response.stream_to_file(f"{wd}/openai_speech/{self.rand}_tts_{str_input[:10]}.mp3")

    def new_rand_id(self):
        self.rand = random.randint(100, 1000)

    def get_rand_id(self):
        return self.rand

    @staticmethod
    def __mkdir(name):
        try:
            os.mkdir(name)
        except FileExistsError:
            pass
