from context import src
from context import lib
from src import *
from lib import *


"""
Wrapper functions
"""


def create_creator_formula(py_service_name, code_lines: [str]):
    try:
        formula = ManageFormula()
        for line in code_lines:
            formula.append_code(line)
        formula.save_generated_script(py_service_name)
    except Exception as e:
        return e
    return 200


def delete_creator_formula(py_service_name):
    try:
        ManageFormula().delete_generated_script(py_service_name)
    except Exception as e:
        return e
    return 200



if __name__ == '__main__':
    pg.verify_cfg()
    v1 = pg.main_menu("creator")
    if v1 == 'custom':  # Custom creator method
        lines = []

        # Pick the canvas
        v2 = PickerPage(['NineBySixteen', 'SixteenByNine']).prompt()
        if v2 == 0:  # 9x16
            v3 = PickerPage(['High Resolution', 'Low Resolution'])
            if v3 == 0:
                lines.append("canvas = NineBySixteen('1080x1920')")
            else:
                lines.append("canvas = NineBySixteen('720x1280')")
        if v2 == 1:  # 16x9
            v3 = PickerPage(['High Resolution', 'Low Resolution'])
            if v3 == 0:
                lines.append("canvas = SixteenByNine('1080x1920')")
            else:
                lines.append("canvas = SixteenByNine('720x1280')")

        db = DbNasConnection()


        # Apply edits
        contd = True
        while contd:
            PickerPage([''])


    # Example code for rendering
    # canvas = NineBySixteen('720x1280')
    # video = VideoCompiler(canvas)
    #
    # edit1 = AppendAudio('/Users/dvoicu/mnt/AUUGHHH Tik Tok Sound Effect.mp3')
    #
    # param = TextParam()
    # param.set_font('arial', 40)
    # param.set_font_color('white', 'transparent')
    # param.set_font_outline('black', 1)
    #
    # edit2 = AppendSubtitles()
    # edit2.set_text(param)
    # edit2.set_whisper_model('base')
    # edit2.set_text_location(('center', 'center'))
    # edit2.set_max_word_per_line(4)
    # edit2.set_audio_to_transcribe('/Users/dvoicu/mnt/AUUGHHH Tik Tok Sound Effect.mp3')
    #
    # edit3 = AppendBlur()
    #
    # list_edits = [edit1, edit3, edit2]
    #
    # video.apply_edits(list_edits)
    #
    # video.render()
