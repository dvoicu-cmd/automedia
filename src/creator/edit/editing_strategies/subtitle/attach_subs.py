# Subtitle imports
import os
import shutil
import tempfile
import whisper
from whisper.utils import get_writer

# MoviePy imports
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
from moviepy.video.tools.subtitles import SubtitlesClip

# Text import
from .text_parameters import TextParam

# Import edit
from src.creator.edit.edit import Edit


class AttachSubtitles(Edit):
    """
    Takes in the audio of the most recent current compound video and appends subtitles to it.
    """
    def __init__(self, audio_path: str):
        """
        Initizlizes video to have subtitles
        """
        self.__text = TextParam()
        self.__text_location = ('center', 'center')
        self.__whisper_model = 'base'
        self.__max_words_per_line = 1
        self.__audio_to_transcribe_path = audio_path

    def set_text(self, text_param: TextParam):
        """
        Sets the param properties for text
        :param text_param:
        :return:
        """
        self.__text = text_param

    def set_max_word_per_line(self, num: int):
        self.__max_words_per_line = num

    def set_text_location(self, loc: tuple):
        """
        :param loc: a tuple of size two specifying the x and y location of the subtitles.
        Could also be described with two strings, ex: ('center', 'center') or ('center', 'bottom')
        :return:
        """
        self.__text_location = loc

    def set_whisper_model(self, model: str):
        """
        Sets the model for openAI's whisper
        https://github.com/openai/whisper
        :param model: tiny, base, small, medium, large
        :return:
        """
        self.__whisper_model = model

    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        """
        Execs the subtitles
        """
        # ---- WHISPER ----
        # First render the transcription from whisper
        model = whisper.load_model(self.__whisper_model)
        result = model.transcribe(audio=self.__audio_to_transcribe_path, language="en", word_timestamps=True)

        # Save tmp text file
        temp_text_path = tempfile.mktemp(suffix=".txt")
        with open(temp_text_path, "w") as text_file:
            text_file.write(result["text"])

        # make a dir with the srt file
        output_dir = f"{os.getcwd()}/srt_tmp"

        # If the directory does not exist, create it bozo.
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        # Write the srt file
        srt_writer = get_writer("srt", output_dir)
        srt_writer(result, temp_text_path, {"max_words_per_line": self.__max_words_per_line})

        # Read the file writen
        srt_files = [f for f in os.listdir(output_dir) if f.endswith(".srt")]
        srt_file_path = os.path.join(output_dir, srt_files[0])

        # ---- MOVIEPY ----

        subtitles = SubtitlesClip(srt_file_path, self.__text_generator)
        subtitles = subtitles.set_position(self.__text_location)

        output = CompositeVideoClip([composite_clip, subtitles])

        # Remove the srt file.
        os.remove(srt_file_path)
        try:
            os.rmdir(output_dir)
        except OSError:
            shutil.rmtree(output_dir)
        return output

    def duration(self) -> int:
        # The duration of subtitles is the same duration as duration for the audio clip it transcribes
        audio_duration = AudioFileClip(self.__audio_to_transcribe_path).duration
        return audio_duration

    def __text_generator(self, string_txt):
        return TextClip(
            string_txt,
            font=self.__text.font,
            fontsize=self.__text.size,
            color=self.__text.color,
            bg_color=self.__text.bg_color,
            stroke_color=self.__text.outline_color,
            stroke_width=self.__text.outline_width
        )
