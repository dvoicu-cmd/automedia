from context import src
from context import lib
from src import *
from lib import *


"""
Wrapper functions
"""


def main():
    pg.verify_cfg()
    v1 = pg.main_menu("Creator")
    if v1 == 'custom':

        # CUSTOM CREATOR FORMULA CREATION

        f = ManageFormula()

        service_name = InputPage("Give a title to the service:").prompt()

        f.ap("""
        
manager = CreatorDirManager()
output_tmp = manager.create_tmp_dir("am_i_the_a_hole_upload")
db = DbNasConnection()

print("-> Created DbNas Connection")
        
        """)

        # Pick the canvas
        v2 = PickerPage(['NineBySixteen', 'SixteenByNine']).prompt("Pick a canvas size: width by height")
        if v2 == 0:  # 9x16
            v3 = PickerPage(['High Resolution: 1080x1920', 'Low Resolution: 720x1280']).prompt("Enter a resolution")
            if v3 == 0:
                f.ap("canvas = NineBySixteen('1080x1920')")
            else:
                f.ap("canvas = NineBySixteen('720x1280')")
        if v2 == 1:  # 16x9
            v3 = PickerPage(['High Resolution: 1080x1920', 'Low Resolution: 720x1280']).prompt("Enter a resolution")
            if v3 == 0:
                f.ap("canvas = SixteenByNine('1080x1920')")
            else:
                f.ap("canvas = SixteenByNine('720x1280')")
        f.ap('base = VideoSection(canvas=canvas)')

        # Set up edits
        f.ap('# -------- Set up the edits --------')
        f.ap('edits = []')

        # prompt for media_pool_ids
        text_content = InputPage("Input the media pool id for the story content (integer)").prompt()
        num_text_content = InputPage("Input the number of stories to load from the media pool").prompt()

        f.ap(f"""
        
media_pool_id = {text_content}
num_story = {num_text_content}
i = 1 
        """)

        # Prompt to archive
        archive = PickerPage(["Yes", "No"]).prompt("Do you wish to archive the text content after use?")

        # Reads in the stories
        f.ap("""
        
record = db.read_rand_media_file_of_pool(media_pool_id)
story_text = manager.read_text(db.nas_root() + "/" + record[1])

        """)

        if archive == 0:
            f.ap("""
            
db.update_to_archived("media_files", record[0])

        """)

        f.ap("""
        
while i <= num_story:
    add_record = db.read_rand_media_file_of_pool(media_pool_id)
    story_text = story_text + " ... Next story. "
    story_text = story_text + manager.read_text(db.nas_root() + "/" + db.read_rand_media_file_of_pool(media_pool_id)[1])
    i = i + 1
        
        """)

        if archive == 0:
            f.ap("""
            
    f.ap('db.update_to_archived("media_files", add_record[0])')
            
            """)

        # Call some tts
        tts_name = InputPage("Give a tts voice: alloy, echo, fable, onyx, nova, or shimmer").prompt()
        f.ap(f"""
        
# Call a tts
tts_tmp = manager.create_tmp_dir()
story_narration = OpenAiAPI().text_to_speech("{tts_name}", story_text, tts_tmp)
narration = AttachAudio(manager.select_dir_one(tts_tmp))
        
        """)

        max_word_per_line = InputPage("SUBS: Input the max words per line").prompt()
        font = InputPage("SUBS: Input a valid font: \n Recommended: Arial-Bold").prompt()
        font_size = InputPage("SUBS: Input a font size. \n Recommended: 96").prompt()
        font_outline = InputPage("SUBS: Input size of font outline. \n Recommended: 4").prompt()
        whisper_model = InputPage("SUBS: Enter transcription accuracy: tiny, base, small, medium, large \n Recommended medium for optimal render time and accuracy").prompt()


        f.ap(f"""
        
# Create subtitles
subs = AttachSubtitles(manager.select_dir_one(tts_tmp))
txt = TextParam()
txt.set_font('{font}', {font_size})
txt.set_font_outline('black', {font_outline})
txt.set_font_color('white', 'transparent')
subs.set_text(txt)
subs.set_whisper_model('{whisper_model}')
subs.set_text_location(('center', 'center'))
subs.set_max_word_per_line({max_word_per_line})
        
        """)


        # Setting footage size.
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
    # Find way to stretch video vertically wider
    record = db.read_rand_media_file_of_pool({footage_id})
    e = AttachMuteVideo(db.nas_root() + "/" + record[1], ('center', 'center'))  # get random parkour footage
    e.set_start_and_end(footage_duration_sum, e.duration())  # set times
    e.resize({width}, {height})
    list_of_footage.append(e)  # add the footage to the list
    footage_duration_sum += e.duration()  # add to sum
    
    """)
        if archive == 0:
            f.ap(f"""
            
    db.update_to_archived("media_files", record[0])
    
            """)

        f.ap(f"""
        
print("-> Got Edits")

# append the edits
edits.extend(list_of_footage)
edits.append(narration)
edits.append(subs)

print("-> Applying Edits")

# apply the edits
base.apply_edits(edits, narration)

print("-> Applied, Rendering Video:")

        """)

        f.ap("""
        
# render footage to output dir
base.render(f"{output_tmp}/video.mp4")

        """)

        make_thumb = PickerPage(["Yes", "No"]).prompt("Do you wish to create a thumbnail with your content? \n"
                                                      "This only applies to YT uploads")
        if make_thumb == 0:
            base_image = InputPage("Input the media pool with your base thumbnail image").prompt()
            archive = PickerPage(["Yes", "No"]).prompt("Do you wish to archive the thumbnail after use?\n"
                                                       "Ensure that you have a constant supply of thumbnail images if you do.")

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
ttxt.font = cv2.FONT_HERSHEY_PLAIN
ttxt.position = (60, 540)
ttxt.font_color = (0, 0, 0)
ttxt.font_scale = 6
ttxt.thickness = ttxt.font_scale * 2
ttxt.limit_words(16, 5)  # Each line can hold about 38 characters. average word is 4.7 characters.
thumb.place_text(ttxt)

            """)

            f.ap('# Write thumbnail')
            f.ap('thumb.write(2, f"{output_tmp}", "thumbnail")')
            if archive == 0:
                f.ap('db.update_to_archived("media_files", record[0])')

        elif make_thumb == 1:
            f.ap("""
            
# Create post title (NO THUMBNAIL OPTION SELECTED)
ttxt = ThumbnailText(story_text)
ttxt.limit_words(16, 5)
            
            """)

        description = InputPage("Input a generic description that will be posted on all your videos?").prompt()
        account_name = InputPage("Input the associated account name this content will be uploaded to").prompt()

        f.ap(f"""
        
print("-> Uploading to DbNas")

# upload to db nas
db.create_content(output_tmp, ttxt.text_content, "{description}", "{account_name}")

# clean the tmp dirs
manager.cleanup(tts_tmp)
        
        """)

        # Save the script
        f.save_generated_script(service_name)

        InputPage.clear()
        print(f"Created Service File: {service_name}")
        print(200)

    # end of custom

    if v1 == 'manual':
        inputs = [
            InputPage("Manually uploading content file:\n Input the absolute file location of the contents you wish to upload").prompt(),
            InputPage("Input the title of the content:").prompt(),
            InputPage("Input a description for the content file(s):").prompt(),
            InputPage("Input the associated name of the account that these contents are related to:").prompt()
        ]
        try:
            db = DbNasConnection()
            db.create_content(*inputs)
        except Exception as e:
            raise e
        print(200)



if __name__ == '__main__':
    main()

