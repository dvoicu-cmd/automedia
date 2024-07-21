import os
import sys

from lib.manage_formula.manage_formula import ManageFormula
from lib.cli_interface.page.input_pages import InputPage
from lib.cli_interface.page.picker_pages import PickerPage


class CreatorFormulas:
    def __init__(self):
        pass

    @staticmethod
    def generic_text_story():

        # Steps in a generic multi story text formula
        # 1) Create dir manager, db connection, and edits list
        # 2) Set up video canvas
        # 3) Set up story content, and multiple stories based on video length and/or specified minimum number of stories
        # 4) Set up subtitles and narration
        # 5) Set background content
        # 6) Glue it all together and render
        # 7) Optional, make a short version of the video.
        # 8) Optional, make a thumbnail.
        # 9) Upload it to db

        f = ManageFormula()

        service_name = InputPage("Give a title to the service:").prompt()

        # ----------------- 1) init -----------------

        CreatorFormulas.__init_formula(f, name=service_name)

        # ----------------- 2) Canvas Options -----------------

        CreatorFormulas.__canvas_options(f)

        # ----------------- 3) Media Pool Selection Options -----------------

        # prompt for media_pool_ids
        text_content = InputPage("Input the media pool id for the story content").prompt()

        f.ap(f"""
        
media_pool_id = {text_content}
i = 1 
        """)

        # Read in at the minimum one text story.
        f.ap("""

record = db.read_rand_media_file_of_pool(media_pool_id)
story_text = manager.read_text(db.nas_root() + "/" + record[1])

        """)

        # Prompt to archive
        archive = PickerPage(["Yes", "No"]).prompt("Do you wish to archive the text content after use?")

        if archive == 0:
            f.ap("""

# Archive option selected
db.update_to_archived("media_files", record[0])

        """)

        # ----------------- 3) Apply Multiple Stories -----------------

        num_text_content = InputPage("Input the number of stories to load from the media pool").prompt()

        f.ap(f"""
        
num_story = {num_text_content}
        
while i <= num_story:
    add_record = db.read_rand_media_file_of_pool(media_pool_id)
    story_text = story_text + " ... Next story. "
    story_text = story_text + manager.read_text(db.nas_root() + "/" + db.read_rand_media_file_of_pool(media_pool_id)[1])
    i = i + 1
        
        """)

        if archive == 0:
            f.ap("""
            
    # Archive option selected
    db.update_to_archived("media_files", add_record[0])
            
            """)

        # ----------------- 3) Minimum Video Length Options -----------------

        have_min_length = PickerPage(["Yes", "No"]).prompt("Do you wish to have a minimum duration for videos")

        if have_min_length == 0:
            min_length = InputPage("Input the minimum length you wish to have for a video in min").prompt()
            f.ap(f"""
            
# Selected Option to have a minimum story length
min_len = {min_length}

while OpenAiAPI.estimate_tts_time(story_text) < min_len:
    add_record = db.read_rand_media_file_of_pool(media_pool_id)
    story_text = story_text + " ... Next story. "
    story_text = story_text + manager.read_text(db.nas_root() + "/" + db.read_rand_media_file_of_pool(media_pool_id)[1])
            
            """)

        if archive == 0:
            f.ap("""

    # Archive option selected
    db.update_to_archived("media_files", add_record[0])

            """)

        # ----------------- 4) Apply Subtitles -----------------

        CreatorFormulas.__tts_and_subs(f)

        # ----------------- 5) Media Pool Background Footage Selection -----------------

        CreatorFormulas.__background_footage_options(f)

        # ----------------- 6) Final Application of Edits -----------------

        f.ap("""
        
print("-> Got Edits")

# append the edits
edits.extend(list_of_footage)
edits.append(narration)
edits.append(subs)

print("-> Applying Edits")

# apply the edits
base.apply_edits(edits, narration)

print("-> Applied, Rendering Video:")
base.render(f"{output_tmp}/video.mp4")

        """)

        # ----------------- 7) Shortify Options -----------------

        make_short = PickerPage(["Yes", "No"]).prompt("Do you wish to create a short form version of this video? \n"
                                                     "This creates a copy of the video in a NineBySixteen format and is cropped to under a one minute")
        if make_short:
            f.ap("""
            
print("-> Creating Short")

short_canvas = NineBySixteen('1080x1920')
short_base = VideoSection(canvas=short_canvas)
narration.set_start_and_end(0, 59)
subs.set_max_word_per_line(2)

print("-> Applying Edits")
short_base.apply_edits(edits, narration)

print("-> Applied, Rendering Video:")
short_base.render(f"{output_tmp}/short.mp4")

            """)

        # ----------------- 8) Thumbnail Options -----------------

        CreatorFormulas.__thumbnail_options(f)

        # ----------------- 9) DB Upload Options -----------------

        description = InputPage("Input a generic description that will be posted on all your videos?").prompt()
        account_name = InputPage("Input the associated account name this content will be uploaded to").prompt()

        f.ap(f"""
        
print("-> Uploading to DbNas")
print("-> File:")
print(output_tmp)

# upload to db nas
db.create_content(output_tmp, ttxt.text_content, "{description}", "{account_name}")

# clean the tmp dirs
manager.cleanup(tts_tmp)
        
        """)

        # Save the script
        f.save_generated_script(service_name)



    @staticmethod
    def cycling_images_story():

        # 1) Create dir manager, db connection, and edits list
        # 2) Set up video canvas
        # 3) Set up story content
        # 4) Set up narration and subtitles
        # 5) Set background content
        # 6) Set a cyclical image edit and place it
        # 7) Glue it all together and render
        # 8) Optional, make a short version of the video.
        # 9) Optional, make a thumbnail.
        # 10) Upload to db

        f = ManageFormula()

        service_name = InputPage("Give a title to the service:").prompt()

        # ----------------- 1) Init -----------------

        CreatorFormulas.__init_formula(f, name=service_name)

        # ----------------- 2) Canvas Options -----------------

        CreatorFormulas.__canvas_options(f)

        # ----------------- 3) Set up story content -----------------

        content = InputPage("Input the media pool id for the text with image content").prompt()
        archive = PickerPage(["Yes", "No"]).prompt("Do you wish to archive the content after use?")

        f.ap(f"""

media_pool_id = {content}
        
            """)

        f.ap("""

record = db.read_rand_media_file_of_pool(media_pool_id)
content_dir = db.nas_root() + "/" + record[1]
story_text = manager.read_text(db.nas_root() + "/" + record[1] + "/text.txt")
image_locations = manager.select_dir(content_dir, file_filter="*.jpg")
        
            """)

        if archive == 0:
            f.ap("""

# Archive option selected
db.update_to_archived("media_files", record[0])

                """)

        # ----------------- 4) Set up narration and subtitles -----------------

        CreatorFormulas.__tts_and_subs(f)

        # ----------------- 5) Set background content -----------------

        CreatorFormulas.__background_footage_options(f)

        # ----------------- 6) Set a cyclical image edit and place it -----------------

        between_time = InputPage("Input the time in seconds, how long each image will be shown for.").prompt()
        img_x = InputPage("Input the x position of the images.\n"
                          "Your input can be a number or a string like: \"center\", \"top\", \"bottom\"").prompt()
        img_y = InputPage("Input the y position of the images.\n"
                          "Your input can be a number or a string like: \"center\", \"top\", \"bottom\"").prompt()

        if isinstance(img_x, int) and isinstance(img_y, int):
            f.ap(f"""
        
# Make the image cycle
img_cycle = AttachCyclicalImages(image_locations, {between_time}, ({img_x}, {img_y}))

            """)

        elif isinstance(img_y, int):

            f.ap(f"""
        
# Make the image cycle
img_cycle = AttachCyclicalImages(image_locations, {between_time}, ("{img_x}", {img_y}))

            """)

            pass

        elif isinstance(img_x, int):
            f.ap(f"""
        
# Make the image cycle
img_cycle = AttachCyclicalImages(image_locations, {between_time}, ({img_x}, "{img_y}"))

            """)

        else:
            f.ap(f"""
        
# Make the image cycle
img_cycle = AttachCyclicalImages(image_locations, {between_time}, ("{img_x}", "{img_y}"))

            """)

        # ----------------- 7) Glue it all together and render -----------------

        f.ap("""
        
# append the edits
edits.extend(list_of_footage)
edits.append(narration)
edits.append(img_cycle)
edits.append(subs)

print("-> Applying Edits")
base.apply_edits(edits, narration)

print("-> Applied, Rendering Video:")
base.render(f"{output_tmp}/video.mp4")

        """)

        # ----------------- 8) Optional, make a short version of the video. -----------------

        make_short = PickerPage(["Yes", "No"]).prompt("Do you wish to create a short form version of this video? \n"
                                                      "This creates a copy of the video in a NineBySixteen format and is cropped to under a one minute")
        if make_short == 0:
            f.ap("""

print("-> Creating Short Version")
# Remove the narration, img_cycle, and subs to modify them for a short version.
edits.pop()
edits.pop()
edits.pop()

# Make a short canvas
short_canvas = NineBySixteen('1080x1920')
short_base = VideoSection(canvas=short_canvas)

# Force everything to the center and reduce the narration to under one min
narration.set_start_and_end(0, 59)
img_cycle.set_location(('center', 'center'))
subs.set_text_location(('center', 'center'))
subs.set_max_word_per_line(2)

print("-> Applying Edits")
edits.append(narration)
edits.append(img_cycle)
edits.append(subs)
short_base.apply_edits(edits, narration)

print("-> Applied, Rendering Video:")
short_base.render(f"{output_tmp}/short.mp4")

            """)

        # ----------------- 9) Optional, make a thumbnail. -----------------

        CreatorFormulas.__thumbnail_options(f)

        # ----------------- 10) Upload to db. -----------------
        description = InputPage("Input a generic description that will be posted on all your videos?").prompt()
        account_name = InputPage("Input the associated account name this content will be uploaded to").prompt()

        f.ap(f"""

print("-> Uploading to DbNas")
print("-> File:")
print(output_tmp)

# upload to db nas
db.create_content(output_tmp, ttxt.text_content, "{description}", "{account_name}")

# clean the tmp dirs
manager.cleanup(tts_tmp)

            """)

        f.save_generated_script(service_name)
        pass

    @staticmethod
    def cycling_images_story_shorts():
        # 1) Create dir manager, db connection, and edits list
        # 2) Set up video canvas
        # 3) Set up story content
        # 4) Set up narration and subtitles
        # 5) Set background content
        # 6) Set a cyclical image edit and place it
        # 7) Glue it all together and render
        # 10) Upload to db

        f = ManageFormula()

        service_name = InputPage("Give a title to the service:").prompt()

        # ----------------- 1) Init -----------------

        CreatorFormulas.__init_formula(f, name=service_name)

        # ----------------- 2) Canvas Options -----------------

        # This is automatically set to 9:16

        # ----------------- 3) Set up story content -----------------

        content = InputPage("Input the media pool id for the text with image content").prompt()
        archive = PickerPage(["Yes", "No"]).prompt("Do you wish to archive the content after use?")

        f.ap(f"""

media_pool_id = {content}
        
            """)

        f.ap("""

record = db.read_rand_media_file_of_pool(media_pool_id)
content_dir = db.nas_root() + "/" + record[1]
story_text = manager.read_text(db.nas_root() + "/" + record[1] + "/text.txt")
image_locations = manager.select_dir(content_dir, file_filter="*.jpg")
        
            """)

        if archive == 0:
            f.ap("""

# Archive option selected
db.update_to_archived("media_files", record[0])

                """)

        # ----------------- 4) Set up narration and subtitles -----------------

        CreatorFormulas.__tts_and_subs(f)

        # ----------------- 5) Set background content -----------------

        CreatorFormulas.__background_footage_options(f)

        # ----------------- 6) Set a cyclical image edit and place it -----------------

        between_time = InputPage("Input the time in seconds, how long each image will be shown for.").prompt()
        f.ap(f"""
img_cycle = AttachCyclicalImages(image_locations, {between_time}, ('center', 'center'))
        """)

        # ----------------- 7) Glue it all together and render -----------------

        f.ap("""
# append the edits
edits.extend(list_of_footage)

# Make a short canvas
short_canvas = NineBySixteen('1080x1920')
short_base = VideoSection(canvas=short_canvas)

# Force everything to the center and reduce the narration to under one min if it's longer.
if narration.duration() > 59:
    narration.set_start_and_end(0, 59)

subs.set_text_location(('center', 'center'))
subs.set_max_word_per_line(2)

print("-> Applying Edits")
edits.append(narration)
edits.append(img_cycle)
edits.append(subs)
short_base.apply_edits(edits, narration)

print("-> Applied, Rendering Video:")
short_base.render(f"{output_tmp}/video.mp4")

        """)

        # ----------------- 8) Upload to db. -----------------
        description = InputPage("Input a generic description that will be posted on all your videos?").prompt()
        account_name = InputPage("Input the associated account name this content will be uploaded to").prompt()

        f.ap(f"""

print("-> Uploading to DbNas")
print("-> File:")
print(output_tmp)

# NO THUMBNAIL OPTION SELECTED
# Create post title
ttxt = ThumbnailText(story_text)
ttxt.limit_words(16, 5)

# upload to db nas
db.create_content(output_tmp, ttxt.text_content, "{description}", "{account_name}")

# clean the tmp dirs
manager.cleanup(tts_tmp)

            """)

        f.save_generated_script(service_name)
        pass

    # ----------------------------------------------------------------------------------
    # ------------------------------ Common Functionality ------------------------------
    # ----------------------------------------------------------------------------------


    @staticmethod
    def __init_formula(f: ManageFormula, name="_"):
        f.ap(f"""

manager = CreatorDirManager()
output_tmp = manager.create_tmp_dir("{name}") 
db = DbNasConnection()

print("-> Created DbNas Connection")
 
        """)
        f.ap('# -------- Set up the edits --------')
        f.ap('edits = []')


    @staticmethod
    def __canvas_options(f: ManageFormula):

        # Pick the canvas
        v2 = PickerPage(['NineBySixteen', 'SixteenByNine']).prompt("Pick a canvas size: width by height")
        if v2 == 0:  # 9x16
            v3 = PickerPage(['High Resolution: 1080x1920', 'Low Resolution: 720x1280']).prompt("Enter a resolution")
            if v3 == 0:
                f.ap("canvas = NineBySixteen('1080x1920')")
            else:
                f.ap("canvas = NineBySixteen('720x1280')")
        if v2 == 1:  # 16x9
            v3 = PickerPage(['High Resolution: 1920x1080', 'Low Resolution: 1280x720']).prompt("Enter a resolution")
            if v3 == 0:
                f.ap("canvas = SixteenByNine('1920x1080')")
            else:
                f.ap("canvas = SixteenByNine('1280x720')")
        f.ap('base = VideoSection(canvas=canvas)')

    @staticmethod
    def __tts_and_subs(f: ManageFormula):

        # Apply TTS Options
        tts_name = InputPage("Give a tts voice: alloy, echo, fable, onyx, nova, or shimmer").prompt()

        f.ap(f"""

# Call a tts
manager.new_rand_id()
tts_tmp = manager.create_tmp_dir()
story_narration = OpenAiAPI().text_to_speech("{tts_name}", story_text, tts_tmp)
narration = AttachAudio(manager.select_dir_one(tts_tmp))

            """)

        # Apply Subtitle Options
        max_word_per_line = InputPage("SUBS: Input the max words per line").prompt()
        font = InputPage("SUBS: Input a valid font: \n Recommended: Helvetica-Bold").prompt()
        font_size = InputPage("SUBS: Input a font size. \n Recommended: 96").prompt()
        font_outline = InputPage("SUBS: Input size of font outline. \n Recommended: 4").prompt()
        font_loc_x = InputPage("SUBS: Input the x position of the subtitles.\n"
                               "Your input can be a number or a string like: \"center\", \"top\", \"bottom\"").prompt()
        font_loc_y = InputPage("SUBS: Input the y position of the subtitles.\n"
                               "Your input can be a number or a string like: \"center\", \"top\", \"bottom\"").prompt()
        whisper_model = InputPage(
            "SUBS: Enter transcription accuracy: tiny, base, small, medium, large \n"
            "Recommended medium for optimal render time and accuracy").prompt()

        f.ap(f"""

# Create subtitles
subs = AttachSubtitles(manager.select_dir_one(tts_tmp))
txt = TextParam()
txt.set_font('{font}', {font_size})
txt.set_font_outline('black', {font_outline})
txt.set_font_color('white', 'transparent')
subs.set_text(txt)
subs.set_whisper_model('{whisper_model}')
subs.set_max_word_per_line({max_word_per_line})

            """)

        if isinstance(font_loc_x, int) and isinstance(font_loc_y, int):
            f.ap(f"subs.set_text_location(({font_loc_x}, {font_loc_y}))")
        elif isinstance(font_loc_y, int):
            f.ap(f"subs.set_text_location((\"{font_loc_x}\", {font_loc_y}))")
        elif isinstance(font_loc_x, int):
            f.ap(f"subs.set_text_location(({font_loc_x}, \"{font_loc_y}))\"")
        else:
            f.ap(f"subs.set_text_location((\"{font_loc_x}\", \"{font_loc_y}\"))")


    @staticmethod
    def __background_footage_options(f: ManageFormula):
        footage_id = InputPage("Input the media pool id from which you wish to pull background footage from").prompt()

        width = 0
        height = 0

        expected_aspect = PickerPage(['NineBySixteen', 'SixteenByNine']).prompt(
            "What is the expected aspect ratio of the media pool's content?")
        if expected_aspect == 0:
            width = 1920
            height = 1080
        elif expected_aspect == 1:
            width = 1080
            height = 1920

        double_size = PickerPage(["Yes", "No"]).prompt("Do you wish to double the size of the background footage?")

        if double_size == 0:
            width = width * 2
            height = height * 2
        elif double_size == 1:
            pass

        archive = PickerPage(["Yes", "No"]).prompt("Do you wish to archive the footage after use?")

        f.ap(f"""
        
# You need to count the length of the story narration as that is the edit that determines the duration.
list_of_footage = []

footage_duration_sum = 0
while footage_duration_sum < narration.duration():
    record = db.read_rand_media_file_of_pool({footage_id})
    e = AttachMuteVideo(db.nas_root() + "/" + record[1], ('center', 'center'))
    e.set_start_and_end(footage_duration_sum, e.duration())
    e.resize({width}, {height})
    list_of_footage.append(e)
    footage_duration_sum += e.duration()
    
    """)

        if archive == 0:
            f.ap(f"""
            
    db.update_to_archived("media_files", record[0])
    
            """)

    @staticmethod
    def __thumbnail_options(f: ManageFormula):
        # ----------------- Thumbnail Options -----------------

        make_thumb = PickerPage(["Yes", "No"]).prompt("Do you wish to create a thumbnail with your content? \n"
                                                      "This only applies to YT uploads")
        if make_thumb == 0:
            base_image = InputPage("Input the media pool's id with your base thumbnail image").prompt()
            archive = PickerPage(["Yes", "No"]).prompt("Do you wish to archive the thumbnail after use?\n"
                                                       "Ensure that you have a constant supply of thumbnail images if you do.")

            font = InputPage("Input the font you wish to use. \n"
                             "Valid Options: simplex, plain, duplex, complex, triplex, small, s_simplex, s_complex\n"
                             "Recommended: simplex").prompt()
            font_scale = InputPage("Input the font scale you wish to use. (Integer)\n"
                                   "Recommended: 6").prompt()
            font_thickness = InputPage("Input the font thickness you wish to use. (Integer)\n"
                                       "Recommended: 12").prompt()
            font_pos_x = InputPage("Input the x pixel position you wish to place the text\n"
                                   "Text is placed from the top left corner of the first character\n"
                                   "Recommended for reddit thumbnails: 75").prompt()
            font_pos_y = InputPage("Input the y pixel position you wish to place the text\n"
                                   "Recommended for reddit thumbnails: 540").prompt()
            # The maximum total number of words shown in the thumbnail text
            max_total_words = InputPage("Input the maximum number of words you wish to have in the thumbnail text.\n"
                                        "Recommended for reddit thumbnails: 15").prompt()
            # Each line can hold 38ish characters in reddit thumbnails I've tested. The average word is 4.7 characters.
            words_per_line = InputPage("Input the maximum number of words you wish to have per line in the thumbnail text\n"
                                       "Recommended for reddit thumbnails: 5").prompt()

            highlights = PickerPage(["Highlights", "Random Highlights", "No Highlights"]).prompt("Do you wish for the thumbnail text to have highlights, randomized higlights, or no highlights at all.")
            bg_color = None
            if highlights == 0 or highlights == 1:
                r = InputPage("Inputting the color value for the text highlights\n"
                              "Input from 0 to 255 the Red Value").prompt()
                g = InputPage("Input from 0 to 255 the Green Value").prompt()
                b = InputPage("Input from 0 to 255 the Blue Value").prompt()
                bg_color = (r, g, b)

            f.ap(f"""
            
print("-> Creating Thumbnail")

# create thumbnail
# 0 -> id, 1 -> file_location, 2 -> media_type, 3 -> title, 4 -> description, 5 -> to_archive
record = db.read_rand_media_file_of_pool({base_image})
img_location = db.nas_root() + "/" + record[1]

canvas = SixteenByNine('1920x1080')
thumb = MakeThumbnail(canvas=canvas)
thumb.place_img(img_location, (1920, 1080), (0, 0))

# thumb text
ttxt = ThumbnailText(story_text)
ttxt.set_font_attr("{font}", {font_scale}, {font_thickness}, (0, 0, 0))
ttxt.set_pos({font_pos_x}, {font_pos_y})
ttxt.limit_words({max_total_words}, {words_per_line})
            """)

            # Determining the thumbnail bg color settings
            # Highlight all
            if highlights == 0:
                f.ap(f"""
                
# All Highlights Option Selected
ttxt.set_background((50, 50), {bg_color}, 1)
thumb.place_text(ttxt)
                
                """)

            # Randomize Highlights
            if highlights == 1:
                f.ap(f"""

# Randomized Highlights Option Selected
ttxt.set_background((50, 50), {bg_color}, 1)
thumb.place_text(ttxt, random_bg=True)

                """)

            if highlights == 2:
                f.ap(f"""
               
# No Highlights Option Selected 
thumb.place_text(ttxt)

                """)

            # Write that thumbnail file.
            f.ap("""
            
# Write thumbnail file
thumb.write(2, f"{output_tmp}", "thumbnail")

            """)

            if archive == 0:
                f.ap('db.update_to_archived("media_files", record[0])')

        elif make_thumb == 1:
            f.ap("""
            
# NO THUMBNAIL OPTION SELECTED
# Create post title
ttxt = ThumbnailText(story_text)
ttxt.limit_words(16, 5)
            
            """)

