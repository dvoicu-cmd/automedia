# Subtitle imports
import os
import tempfile
import whisper
from whisper.utils import get_writer

# MoviePy imports
from moviepy.editor import TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip

# Text import
from text_parameters import TextParam

from src.creator.edit.edit import Edit


class AppendSubtitles(Edit):
    def __init__(self, text_param=TextParam):
        """
        Initizlizes video to have subtitles
        """
        self.text = text_param
        self.text_location = ('center', 'center')
        self.whisper_model = 'base'

    def set_text(self, text_param: TextParam):
        self.text = text_param

    def set_whisper_model(self, model: str):
        self.whisper_model = model

    def apply(self, composite_clip: CompositeVideoClip) -> CompositeVideoClip:
        """
        Execs the subtitles
        """
        # ---- WHISPER ----

        # first render the transcription from whisper
        model = whisper.load_model(self.whisper_model)
        result = model.transcribe(audio=composite_clip, language="en", word_timestamps=True)

        # Save tmp text file
        temp_text_path = tempfile.mktemp(suffix=".txt")
        with open(temp_text_path, "w") as text_file:
            text_file.write(result["text"])

        # make a dir with the srt file
        output_dir = f"{os.getcwd()}/srt_tmp"

        # Write the srt file
        srt_writer = get_writer("srt", output_dir)
        srt_writer(result, temp_text_path, {"max_words_per_line": 1})

        # Read the file writen
        srt_files = [f for f in os.listdir(output_dir) if f.endswith(".srt")]
        srt_file_path = os.path.join(output_dir, srt_files[0])

        # ---- MOVIEPY ----

        subtitles = SubtitlesClip(srt_file_path, self.text_generator)
        subtitles = subtitles.set_position(self.text_location)

        output = CompositeVideoClip([composite_clip, subtitles])

        # Remove the srt file.
        os.remove(srt_file_path)
        os.rmdir(output_dir)

        return output

    def text_generator(self, string_txt):
        return TextClip(
            string_txt,
            font=self.text.font,
            fontsize=self.text.size,
            color=self.text.color,
            bg_color=self.text.bg_color,
            stroke_color=self.text.outline_color,
            stroke_width=self.text.outline_width
        )
