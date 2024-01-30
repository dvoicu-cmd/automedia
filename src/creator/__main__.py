from context import src

from src.creator.video_compiler import VideoCompiler
from src.creator.edit import *
from src.creator.canvas import *


if __name__ == '__main__':
    canvas = NineBySixteen('720x1280')
    video = VideoCompiler(canvas)

    edit1 = AppendAudio('/Users/dvoicu/mnt/AUUGHHH Tik Tok Sound Effect.mp3')

    param = TextParam()
    param.set_font('arial', 40)
    param.set_font_color('white', 'transparent')
    param.set_font_outline('black', 1)

    edit2 = AppendSubtitles()
    edit2.set_text(param)
    edit2.set_whisper_model('base')
    edit2.set_text_location(('center', 'center'))
    edit2.set_max_word_per_line(4)
    edit2.set_audio_to_transcribe('/Users/dvoicu/mnt/AUUGHHH Tik Tok Sound Effect.mp3')

    edit3 = AppendBlur()

    list_edits = [edit1, edit3, edit2 ]

    video.apply_edits(list_edits)

    video.render()
