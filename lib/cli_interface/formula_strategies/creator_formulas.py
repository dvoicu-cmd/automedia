from .formulas_interface import InterfaceFormulas

from lib.manage_formula.manage_formula import ManageFormula
from lib.cli_interface.page.input_pages import InputPage
from lib.cli_interface.page.picker_pages import PickerPage

# Important common var names in formulas:
# -------
# output_tmp | the output directory for the created contents.
# for example in a formula code: base.render(f"{output_tmp}/video.mp4") exports a video to the tmp output
# -------
# story_text | contains the text content for the video.
# -------
# ttxt | is the thumbnail text.
# -------
# manager | Is the manager object that manages the scripts directory output contents.
# -------
# output_tmp | Is the absolute path for the output directory.


# Other important common items:
# -------
# video.mp4 | The output content that is long
# -------
# short.mp4 | The output content that is short and horizontal
# -------
# thumbnail.jpg | The thumbnail output
# -------
# title.txt | The title for the video
# -------
# desc.txt | The description for the video
# -------
# thumbnail.txt | The thumbnail text
# get any of these files by using the abs path of the manager dir like so: f"{output_tmp}/video.mp4"


class CreatorFormulas:
    def __init__(self):
        pass

    def create_formula(self, formula_method: str, attr_map={}):
        if formula_method == "generic_text_story":
            self.generic_text_story(attr_map=attr_map)
        if formula_method == "cycling_images_story":
            self.cycling_images_story(attr_map=attr_map)
        if formula_method == "cycling_images_story_shorts":
            self.cycling_images_story_shorts(attr_map=attr_map)

    @staticmethod
    def generic_text_story(attr_map={}):

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
        f.set_properties_type("creator", "generic_text_story")


        service_name = InterfaceFormulas.formula_name(f, attr_map)

        # ----------------- 1) init -----------------

        CreatorFormulas.__init_formula(f, name=service_name)

        # ----------------- 2) Canvas Options -----------------

        CreatorFormulas.__canvas_options(f, attr_map)

        # ----------------- 3) Media Pool Selection Options -----------------

        # prompt for media_pool_ids
        text_content = InputPage("Input the media pool id for the story content").prompt(default_value="text_content")
        f.spa("text_content", text_content)

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
        archive = PickerPage(["Yes", "No"]).prompt("Do you wish to archive the text content after use?", suggested_index=attr_map.get("archive"))
        f.spa("archive", archive)

        if archive == 0:
            f.ap("""

# Archive option selected
db.update_to_archived("media_files", record[0])

        """)

        # ----------------- 3) Apply Multiple Stories -----------------

        num_text_content = InputPage("Input the number of stories to load from the media pool").prompt(default_value="num_text_content")
        f.spa("num_text_content", num_text_content)

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

        have_min_length = PickerPage(["Yes", "No"]).prompt("Do you wish to have a minimum duration for videos", suggested_index=attr_map.get("have_min_length"))
        f.spa("have_min_length", have_min_length)

        if have_min_length == 0:
            min_length = InputPage("Input the minimum length you wish to have for a video in min").prompt(default_value=attr_map.get("min_length"))
            f.spa("min_length", min_length)

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

        CreatorFormulas.__tts_and_subs(f, attr_map)

        # ----------------- 5) Media Pool Background Footage Selection -----------------

        CreatorFormulas.__background_footage_options(f, attr_map)

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
                                                     "This creates a copy of the video in a NineBySixteen (Vertical Video | | ) format and is cropped to under a one minute"
                                                      , suggested_index=attr_map.get("make_short"))
        f.spa("make_short", make_short)

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

        CreatorFormulas.__thumbnail_options(f, attr_map)

        # ----------------- 9) DB Upload Options -----------------

        description = InputPage("Input a generic description.").prompt(default_value=attr_map.get("description"))
        f.spa("description", description)


        account_name = InputPage("Input the associated account name this content will be uploaded to").prompt(
            default_value=attr_map.get("account_name")
        )
        f.spa("account_name", account_name)

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
    def cycling_images_story(attr_map={}):

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
        f.set_properties_type("creator", "cycling_images_story")

        service_name = InterfaceFormulas().formula_name(f, attr_map)

        # ----------------- 1) Init -----------------

        CreatorFormulas.__init_formula(f, name=service_name)

        # ----------------- 2) Canvas Options -----------------

        CreatorFormulas.__canvas_options(f, attr_map)

        # ----------------- 3) Set up story content -----------------

        content_media_pool = InputPage("Input the media pool id for the text with image content").prompt(default_value=attr_map.get("content_media_pool"))
        f.spa("content_media_pool", content_media_pool)

        archive = PickerPage(["Yes", "No"]).prompt("Do you wish to archive the content after use?", suggested_index=attr_map.get("archive"))
        f.spa("archive", archive)

        f.ap(f"""

media_pool_id = {content_media_pool}
        
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

        CreatorFormulas.__tts_and_subs(f, attr_map)

        # ----------------- 5) Set background content -----------------

        CreatorFormulas.__background_footage_options(f, attr_map)

        # ----------------- 6) Set a cyclical image edit and place it -----------------

        between_time = InputPage("Input the time in seconds, how long each image will be shown for.").prompt(default_value=attr_map.get("between_time"))
        f.spa("between_time", between_time)

        img_x = InputPage("Input the x position of the images.\n"
                          "Your input can be a number or a string like: \"center\", \"top\", \"bottom\"").prompt(default_value=attr_map.get("img_x"))
        f.spa("img_x", img_x)

        img_y = InputPage("Input the y position of the images.\n"
                          "Your input can be a number or a string like: \"center\", \"top\", \"bottom\"").prompt(default_value=attr_map.get("img_y"))
        f.spa("img_y", img_y)

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
                                                      "This creates a copy of the video in a NineBySixteen format and is cropped to under a one minute",
                                                      suggested_index=attr_map.get("make_short"))
        f.spa("make_short", make_short)

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

        CreatorFormulas.__thumbnail_options(f, attr_map)

        # ----------------- 10) Upload to db. -----------------

        # Change to be prompt instead.
        CreatorFormulas.__generate_description_text(f, attr_map)
        CreatorFormulas.__generate_title_text(f, attr_map)
        CreatorFormulas.__generate_thumbnail_text(f, attr_map)

        description = InputPage("Input a generic description that will be posted on all your videos?").prompt(default_value=attr_map.get("description"))
        f.spa("description", description)


        account_name = InputPage("Input the associated account name this content will be uploaded to").prompt(default_value=attr_map.get("account_name"))
        f.spa("account_name", account_name)

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
    def cycling_images_story_shorts(attr_map={}):
        # 1) Create dir manager, db connection, and edits list
        # 2) Set up video canvas
        # 3) Set up story content
        # 4) Set up narration and subtitles
        # 5) Set background content
        # 6) Set a cyclical image edit and place it
        # 7) Glue it all together and render
        # 10) Upload to db

        f = ManageFormula()
        f.set_properties_type("creator", "cycling_images_story_shorts")

        service_name = InterfaceFormulas().formula_name(f, attr_map)

        # ----------------- 1) Init -----------------

        CreatorFormulas.__init_formula(f, name=service_name)

        # ----------------- 2) Canvas Options -----------------

        # This is automatically set to 9:16

        # ----------------- 3) Set up story content -----------------

        content_media_pool = InputPage("Input the media pool id for the text with image content").prompt(default_value=attr_map.get("content_media_pool"))
        f.spa("content_media_pool", content_media_pool)

        archive = PickerPage(["Yes", "No"]).prompt("Do you wish to archive the content after use?", suggested_index=attr_map.get("archive"))
        f.spa("archive", archive)

        f.ap(f"""

media_pool_id = {content_media_pool}
        
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

        CreatorFormulas.__tts_and_subs(f, attr_map)

        # ----------------- 5) Set background content -----------------

        CreatorFormulas.__background_footage_options(f, attr_map)

        # ----------------- 6) Set a cyclical image edit and place it -----------------

        between_time = InputPage("Input the time in seconds, how long each image will be shown for.").prompt(default_value=attr_map.get("between_time"))
        f.spa("between_time", between_time)

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
        # description = InputPage("Input a generic description that will be posted on all your videos?").prompt(default_value=attr_map.get("description"))
        # f.spa("description", description)


        account_name = InputPage("Input the associated account name this content will be uploaded to").prompt(default_value=attr_map.get("account_name"))
        f.spa("account_name", account_name)

        f.ap(f"""

print("-> Uploading to DbNas")
print("-> File:")
print(output_tmp)

# NO THUMBNAIL OPTION SELECTED
# Create post title
ttxt = ThumbnailText(story_text)
ttxt.limit_words(16, 5)

# upload to db nas
db.create_content(output_tmp, ttxt.text_content, "", "{account_name}")

# clean the tmp dirs
manager.cleanup(tts_tmp)

            """)

        f.save_generated_script(service_name)

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
    def __canvas_options(f: ManageFormula, attr_map={}):
        # Pick the canvas
        resolution = 0
        aspect_ratio = PickerPage(['NineBySixteen (Vertical Video | | )', 'SixteenByNine (Horizontal Video ---)']).prompt("Pick a canvas size: width by height", suggested_index=attr_map.get("aspect_ratio"))
        if aspect_ratio == 0:  # 9x16
            resolution = PickerPage(['High Resolution: 1080x1920', 'Low Resolution: 720x1280']).prompt("Enter a resolution", suggested_index=attr_map.get("resolution"))
            if resolution == 0:
                f.ap("canvas = NineBySixteen('1080x1920')")
            else:
                f.ap("canvas = NineBySixteen('720x1280')")
        if aspect_ratio == 1:  # 16x9
            resolution = PickerPage(['High Resolution: 1920x1080', 'Low Resolution: 1280x720']).prompt("Enter a resolution", suggested_index=attr_map.get("resolution"))
            if resolution == 0:
                f.ap("canvas = SixteenByNine('1920x1080')")
            else:
                f.ap("canvas = SixteenByNine('1280x720')")
        f.ap('base = VideoSection(canvas=canvas)')

        # Save attr for updates
        f.spa("resolution", resolution)
        f.spa("aspect_ratio", aspect_ratio)

    @staticmethod
    def __tts_and_subs(f: ManageFormula, attr_map={}):

        # Apply TTS Options
        tts_name = InputPage("Give a tts voice: alloy, echo, fable, onyx, nova, or shimmer").prompt(default_value=attr_map.get("tts_name"))
        f.spa("tts_name", tts_name)

        f.ap(f"""

# Call a tts
manager.new_rand_id()
tts_tmp = manager.create_tmp_dir()
story_narration = OpenAiAPI().text_to_speech("{tts_name}", story_text, tts_tmp)
narration = AttachAudio(manager.select_dir_one(tts_tmp))

            """)

        # Apply Subtitle Options
        max_word_per_line = InputPage("SUBS: Input the max words per line").prompt(default_value=attr_map.get("max_word_per_line"))
        f.spa("max_word_per_line", max_word_per_line)

        font = InputPage("SUBS: Input a valid font: \n Recommended: Helvetica-Bold").prompt(default_value=attr_map.get("font"))
        f.spa("font", font)

        font_size = InputPage("SUBS: Input a font size. \n Recommended: 96").prompt(default_value=attr_map.get("font_size"))
        f.spa("font_size", font_size)

        font_outline = InputPage("SUBS: Input size of font outline. \n Recommended: 4").prompt(default_value=attr_map.get("font_outline"))
        f.spa("font_outline", font_outline)

        font_loc_x = InputPage("SUBS: Input the x position of the subtitles.\n"
                               "Your input can be a number or a string like: \"center\", \"top\", \"bottom\""
                               ).prompt(default_value=attr_map.get("font_loc_x"))
        f.spa("font_loc_x", font_loc_x)

        font_loc_y = InputPage("SUBS: Input the y position of the subtitles.\n"
                               "Your input can be a number or a string like: \"center\", \"top\", \"bottom\""
                               ).prompt(default_value=attr_map.get("font_loc_y"))
        f.spa("font_loc_y", font_loc_y)

        whisper_model = InputPage(
            "SUBS: Enter transcription accuracy: tiny, base, small, medium, large \n"
            "Recommended \"medium\" for optimal render time and accuracy").prompt(default_value=attr_map.get("whisper_model"))
        f.spa("whisper_model", whisper_model)

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
    def __background_footage_options(f: ManageFormula, attr_map={}):
        background_footage_id = InputPage("Input the media pool id from which you wish to pull background footage from").prompt(default_value=attr_map.get("background_footage_id"))
        f.spa("background_footage_id", background_footage_id)

        width = 0
        height = 0

        background_expected_aspect = PickerPage(['NineBySixteen (Vertical Video | | )', 'SixteenByNine (Horizontal Video ---)']).prompt(
            "What is the expected aspect ratio of the media pool's content?", suggested_index=attr_map.get("background_expected_aspect"))
        f.spa("background_expected_aspect", background_expected_aspect)

        if background_expected_aspect == 0:
            width = 1920
            height = 1080
        elif background_expected_aspect == 1:
            width = 1080
            height = 1920

        double_size = PickerPage(["Yes", "No"]).prompt("Do you wish to double the size of the background footage?", suggested_index=attr_map.get("double_size"))
        f.spa("double_size", double_size)

        if double_size == 0:
            width = width * 2
            height = height * 2
        elif double_size == 1:
            pass

        archive_background = PickerPage(["Yes", "No"]).prompt("Do you wish to archive the footage after use?", suggested_index=attr_map.get("archive_background"))
        f.spa("archive_background", archive_background)

        f.ap(f"""
        
# You need to count the length of the story narration as that is the edit that determines the duration.
list_of_footage = []

footage_duration_sum = 0
while footage_duration_sum < narration.duration():
    record = db.read_rand_media_file_of_pool({background_footage_id})
    e = AttachMuteVideo(db.nas_root() + "/" + record[1], ('center', 'center'))
    e.set_start_and_end(footage_duration_sum, e.duration())
    e.resize({width}, {height})
    list_of_footage.append(e)
    footage_duration_sum += e.duration()
    
    """)

        if archive_background == 0:
            f.ap(f"""
            
    db.update_to_archived("media_files", record[0])
    
            """)

    @staticmethod
    def __thumbnail_options(f: ManageFormula, attr_map={}):
        # ----------------- Thumbnail Options -----------------

        make_thumb = PickerPage(["Yes", "No"]).prompt("Do you wish to create a thumbnail with your content? \n"
                                                      "This only applies to YT uploads", suggested_index=attr_map.get("make_thumb"))
        f.spa("make_thumb", make_thumb)


        if make_thumb == 0:
            thumb_base_image_id = InputPage("Input the media pool's id with your base thumbnail image").prompt(
                default_value=attr_map.get("thumb_base_image_id"))
            f.spa("thumb_base_image_id", thumb_base_image_id)


            archive_thumb = PickerPage(["Yes", "No"]).prompt("Do you wish to archive the thumbnail after use?\n"
                                                       "Ensure that you have a constant supply of thumbnail images if you do."
                                                             , suggested_index=attr_map.get("archive_thumb"))
            f.spa("archive_thumb", archive_thumb)


            thumb_font = InputPage("Input the font you wish to use. \n"
                             "Valid Options: simplex, plain, duplex, complex, triplex, small, s_simplex, s_complex\n"
                             "Recommended: simplex").prompt(default_value=attr_map.get("thumb_font"))
            f.spa("thumb_font", thumb_font)


            thumb_font_scale = InputPage("Input the font scale you wish to use. (Integer)\n"
                                   "Recommended: 6").prompt(default_value=attr_map.get("thumb_font_scale"))
            f.spa("thumb_font_scale", thumb_font_scale)


            thumb_font_thickness = InputPage("Input the font thickness you wish to use. (Integer)\n"
                                       "Recommended: 12").prompt(default_value=attr_map.get("thumb_font_thickness"))
            f.spa("thumb_font_thickness", thumb_font_thickness)


            thumb_font_pos_x = InputPage("Input the x pixel position you wish to place the text\n"
                                   "Text is placed from the top left corner of the first character\n"
                                   "Recommended for reddit thumbnails: 75").prompt(default_value=attr_map.get("thumb_font_pos_x"))
            f.spa("thumb_font_pos_x", thumb_font_pos_x)


            thumb_font_pos_y = InputPage("Input the y pixel position you wish to place the text\n"
                                   "Recommended for reddit thumbnails: 540").prompt(default_value=attr_map.get("thumb_font_pos_y"))
            f.spa("thumb_font_pos_y", thumb_font_pos_y)


            # The maximum total number of words shown in the thumbnail text
            thumb_max_total_words = InputPage("Input the maximum number of words you wish to have in the thumbnail text.\n"
                                        "Recommended for reddit thumbnails: 15").prompt(default_value=attr_map.get("thumb_max_total_words"))
            f.spa("thumb_max_total_words", thumb_max_total_words)


            # Each line can hold 38ish characters in reddit thumbnails I've tested. The average word is 4.7 characters.
            thumb_words_per_line = InputPage("Input the maximum number of words you wish to have per line in the thumbnail text\n"
                                       "Recommended for reddit thumbnails: 5").prompt(default_value=attr_map.get("thumb_words_per_line"))
            f.spa("thumb_words_per_line", thumb_words_per_line)

            thumb_highlights = PickerPage(["Highlights", "Random Highlights", "No Highlights"]).prompt("Do you wish for the thumbnail text to have highlights, randomized higlights, or no highlights at all."
                                                                                                 , suggested_index=attr_map.get("thumb_highlights"))
            f.spa("thumb_highlights", thumb_highlights)

            bg_color = None
            if thumb_highlights == 0 or thumb_highlights == 1:
                bg_highlights_r_scale = InputPage("Inputting the color value for the text highlights\n"
                              "Input from 0 to 255 the Red Value").prompt(default_value=attr_map.get("bg_highlights_r_scale"))
                bg_highlights_g_scale = InputPage("Input from 0 to 255 the Green Value").prompt(default_value=attr_map.get("bg_highlights_g_scale"))
                bg_highlights_b_scale = InputPage("Input from 0 to 255 the Blue Value").prompt(default_value=attr_map.get("bg_highlights_b_scale"))

                f.spa("bg_highlights_r_scale", bg_highlights_r_scale)
                f.spa("bg_highlights_g_scale", bg_highlights_g_scale)
                f.spa("bg_highlights_b_scale", bg_highlights_b_scale)
                bg_color = (bg_highlights_r_scale, bg_highlights_g_scale, bg_highlights_b_scale)

            f.ap(f"""
            
print("-> Creating Thumbnail")

# create thumbnail
# 0 -> id, 1 -> file_location, 2 -> media_type, 3 -> title, 4 -> description, 5 -> to_archive
record = db.read_rand_media_file_of_pool({thumb_base_image_id})
img_location = db.nas_root() + "/" + record[1]

canvas = SixteenByNine('1920x1080')
thumb = MakeThumbnail(canvas=canvas)
thumb.place_img(img_location, (1920, 1080), (0, 0))

# thumb text
ttxt = ThumbnailText(story_text)
ttxt.set_font_attr("{thumb_font}", {thumb_font_scale}, {thumb_font_thickness}, (0, 0, 0))
ttxt.set_pos({thumb_font_pos_x}, {thumb_font_pos_y})
ttxt.limit_words({thumb_max_total_words}, {thumb_words_per_line})
            """)

            # Determining the thumbnail bg color settings
            # Highlight all
            if thumb_highlights == 0:
                f.ap(f"""
                
# All Highlights Option Selected
ttxt.set_background((50, 50), {bg_color}, 1)
thumb.place_text(ttxt)
                
                """)

            # Randomize Highlights
            if thumb_highlights == 1:
                f.ap(f"""

# Randomized Highlights Option Selected
ttxt.set_background((50, 50), {bg_color}, 1)
thumb.place_text(ttxt, random_bg=True)

                """)

            if thumb_highlights == 2:
                f.ap(f"""
               
# No Highlights Option Selected 
thumb.place_text(ttxt)

                """)

            # Write that thumbnail file.
            f.ap("""
            
# Write thumbnail file
thumb.write(2, f"{output_tmp}", "thumbnail")

            """)

            if archive_thumb == 0:
                f.ap('db.update_to_archived("media_files", record[0])')

        elif make_thumb == 1:
            f.ap("""
            
# NO THUMBNAIL OPTION SELECTED
# Create post title
ttxt = ThumbnailText(story_text)
ttxt.limit_words(16, 5)
            
            """)


# -------------------- Generate Text Functions --------------------

    @staticmethod
    def __generate_title_text(f: ManageFormula, attr_map={}):
        """
        Appends a prompt for a llm to specifically make title text and stores it in the output tmp.
        :param f:
        :param attr_map:
        :return: adds in the
        """
        f.ap("""
# -------------- Make Title Text --------------

# Set llm variables
model = "gpt-4"
system_prompt = "You will be given prompts containing the transcription for some video content. This will include all of the text content spoken and displayed in the video. What I want you to do make a title from this video's transcription. Specifically output a very short eye catching title that tells viewers what the video is about and makes them want to click. Here are some examples. Using | or - to split to larger topics '_____ is the king of it all | rules to power'. Short but sweat: 'Crabs vs. The beach'. Nice and long description: 'Placing 100,000 Grass Blocks To Start The Zoo!'. Your title must be around 8 words with 4 words to give or take. Get as many related keywords as you can to maximize search engine results as we want to reach as many people as possible. You will be limited to a total character limit of 100. Under no circumstances do you go over the stated character limit. Do not include any double quotes or single quotes characters in your output."
ai_prompt = story_text


# Prompt by taking the story text
llm_tmp_str = OpenAiAPI().text_llm(model, system_prompt, ai_prompt, to_file=False)

# Save string
TextUtils.write_txt(f"{output_tmp}/title.txt", llm_tmp_str)

# ----------------------------
        """)

    @staticmethod
    def __generate_description_text(f: ManageFormula, attr_map={}):

        f.ap("""

# -------------- Make Description Text Here --------------

# Set llm variables
model = "gpt-4"
system_prompt = "You will be given prompts containing the transcription for some video content. This will include all of the text content spoken and displayed in the video. What I want you to do is make a description from this video's transcription. Specifically output the following format: first make around 150 words worth of descriptive text, then have 4 line breaks, followed by any related hashtags you can attach to this video. Don't include any hashtags in your initial description section before the 4 line breaks. Avoid saying starting your description with 'The video describes ...' or 'He describes this...'. Get as many related keywords as you can to maximize search engine results in both your inital descriptive text and your hashtags as we want to reach as many people possible. You will be limited to a total character limit of 2000. Under no circumstances do you go over the stated character limit. Distribute to the best of your ability the number of character evenly between the descriptive text and the hashtags, giving 1000 characters to the description and 1000 characters to the hashtags. Do not include any double quotes or single quotes characters in your output."
ai_prompt = story_text


# Prompt by taking the story text
llm_tmp_str = OpenAiAPI().text_llm(model, system_prompt, ai_prompt, to_file=False)

# Save string
TextUtils.write_txt(f"{output_tmp}/desc.txt", llm_tmp_str)

# ----------------------------

        """)

    @staticmethod
    def __generate_thumbnail_text(f: ManageFormula, attr_map={}):

        f.ap("""
        
# -------------- Make Thumbnail Text Here --------------

# Set llm variables
model = "gpt-4"
system_prompt = "You will be given prompts containing the transcription for some video content on youtube. This will include all of the text content spoken and displayed in the video. What I want you to do is make some thumbnail text from this video's transcription. Make one and only one short simple statment that will catch the viewers eyes like: 'this happend...' or 'IT'S HERE', or 'WTF, this ____  happend!', or '[x] situation is...' or 'Done!'. You want around 1 to 5 words in your thumbnail text. This will be displayed in large text to the viewr on youtube. Get as many related keywords as you can to maximize search engine results. You will be limited to a total character limit of 20. Under no circumstances do you go over the stated character limit. Do not include any double quotes or single quotes characters in your output."
ai_prompt = story_text


# Prompt by taking the story text
llm_tmp_str = OpenAiAPI().text_llm(model, system_prompt, ai_prompt, to_file=False)

# Save string
TextUtils.write_txt(f"{output_tmp}/thumb.txt", llm_tmp_str)

# ----------------------------


        """)


