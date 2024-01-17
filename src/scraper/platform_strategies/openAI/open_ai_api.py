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

    def text_llm(self, model, system_msg, user_msg, max_tokens=4096):

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=max_tokens
        )
        str_response = response.choices[0].message.content
        self.dm.dl_text(str_response, f"llm_txt_{user_msg[:10]}")

    def stable_diffusion(self, prompt):
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

        https://platform.openai.com/docs/guides/text-to-speech
        """
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=str_input
        )

        wd = f"{self.dm.dl_root()}/audio"
        response.stream_to_file(f"{wd}/{self.dm.get_rand_id()}_tts_{str_input[:10]}.mp3")
