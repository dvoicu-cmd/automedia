from src.creator.video_compiler import VideoCompiler


from src.creator.edit.editing_strategies.audio.audio_edit import AppendAudio
from src.creator.edit.editing_strategies.attach_video_clip.image_edit import AppendImage
from src.creator.edit.editing_strategies.blur.blur_edit import AppendBlur


from src.creator.edit.editing_strategies.subtitle.text_parameters import TextParam
from src.creator.edit.editing_strategies.subtitle.subs_edit import AppendSubtitles



from src.creator.canvas.canvas_init_strategies.nine_by_sixteen import NineBySixteen
from src.creator.canvas.canvas_init_strategies.sixteen_by_nine import SixteenByNine

canvas = NineBySixteen('1080x1920')
vd = VideoCompiler(canvas=canvas)


# Set up the edits
list_of_edits = []


vd.render()
