import pdb

import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

from lib.manage_directory_structure.scraper_dir_manager import ScraperDirManager
from lib.text_util.util import TextUtils

from moviepy.editor import AudioFileClip, concatenate_audioclips


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

        attempts = 3
        response = None

        while attempts >= 0:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}
                    ],
                )
                break
            except openai.BadRequestError as e:
                if attempts <= 0:
                    raise e
                else:
                    attempts = attempts - 1
                    continue
            except openai.RateLimitError as e:
                if attempts <= 0:
                    raise e
                else:
                    print("HIT RATE LIMIT, HALTING PROGRAM FOR 1 MIN")
                    time.sleep(65)
                    print(f"CONTINUING AI PROMPT. {attempts} ATTEMPTS LEFT")
                    attempts = attempts - 1
                    continue

        str_response = response.choices[0].message.content
        if to_file:
            self.dm.dl_text(str_response, f"llm_txt_{user_msg[:10]}", path_dir_output)
            return None
        else:
            return str_response

    def stable_diffusion(self, prompt, path_dir_output='', name=None):
        """
        Creates a 1024x1024 image and downloads it
        https://platform.openai.com/docs/guides/images?context=node
        :param prompt: The string input describing the image to generate
        :param path_dir_output The absolute path of the output directory
        :param name Optional parameter to manually set the name of the file
        :return: Downloads a file in
        """
        attempts = 3
        response = None

        while attempts >= 0:
            try:
                response = self.client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                break
            except openai.BadRequestError as e:
                if attempts <= 0:
                    raise e
                else:
                    attempts = attempts - 1
                    continue
            except openai.RateLimitError as e:
                if attempts <= 0:
                    raise e
                else:
                    print("HIT RATE LIMIT, HALTING PROGRAM FOR 1 MIN")
                    time.sleep(65)
                    print(f"CONTINUING AI PROMPT. {attempts} ATTEMPTS LEFT")
                    attempts = attempts - 1
                    continue

        image_url = response.data[0].url
        if not name:
            self.dm.dl_via_link(image_url, "image", f"sd_{prompt[:10]}", path_dir_output)
        elif name:
            self.dm.dl_via_link(image_url, "image", f"{name}", path_dir_output, use_hash=False)

    @staticmethod
    def estimate_tts_time(str_input):
        """
        Estimates the time it takes for an open ai tts model to read some given text
        :param str_input:
        :return: The amount of time
        """

        # https://community.openai.com/t/tts-talking-speed-words-per-minute/657893/2
        # According to this post, the average wpm for each voice is about 178
        wpm = 178 / 2  # Given some tests, results give half the result. So the tts is slower
        words = TextUtils.split_single_words(str_input)
        num_words = len(words)
        print(num_words)
        speech_time = num_words/wpm
        return speech_time

    def text_to_speech(self, voice, str_input, path_dir_output=''):
        """
        The text to speach models from openAI
        https://platform.openai.com/docs/guides/text-to-speech

        :param voice: alloy, echo, fable, onyx, nova, and shimmer
        :param path_dir_output The absolute path of the output directory. Assumed to be a dir manager.
        :param str_input: text to input
        """
        # Because openAi has a character limit of 4096 per request, you need to chunk your str input.
        # So chunk the requests and then reassemble the audio file
        partitions = TextUtils.split_partition_sentences(str_input, 4096)

        i = 0
        for part in partitions:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=part
            )
            response.stream_to_file(f"{path_dir_output}/{i}_audio_part_{self.dm.get_rand_id()}_.mp3")
            i = i + 1

        # Now patch all parts into one mp3 file
        mp3_parts = self.dm.select_dir(path_dir_output)
        sorted_mp3_parts = sorted(mp3_parts, key=lambda x: os.path.basename(x))  # sort them as the fs would

        # Compile into one audio file
        audio_clips = [AudioFileClip(mp3) for mp3 in sorted_mp3_parts]
        final_clip = concatenate_audioclips(audio_clips)
        final_output = f"{path_dir_output}/{self.dm.get_rand_id()}_tts_{str_input[:10]}.mp3"
        final_clip.write_audiofile(final_output, logger=None)

        # Delete the parts, they are no longer needed.
        for mp3_part in mp3_parts:
            os.remove(mp3_part)


