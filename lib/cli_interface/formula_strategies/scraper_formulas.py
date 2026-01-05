from .formulas_interface import InterfaceFormulas

from lib.manage_formula.manage_formula import ManageFormula
from lib.cli_interface.page.input_pages import InputPage
from lib.cli_interface.page.picker_pages import PickerPage


class ScraperFormulas(InterfaceFormulas):

    def create_formula(self, formula_method: str, attr_map={}):
        if formula_method == "ollama_text":
            self.ollama_text(attr_map=attr_map)
        if formula_method == "ollama_comfy_text_and_img":
            self.ollama_comfy_text_and_img(attr_map=attr_map)
        if formula_method == "comfy_thumb":
            self.comfy_thumb(attr_map=attr_map)
        if formula_method == "reddit_scrape":
            self.reddit_scrape(attr_map=attr_map)
        if formula_method == "open_ai_text":
            self.open_ai_text(attr_map=attr_map)
        if formula_method == "open_ai_text_and_img":
            self.open_ai_text_and_img(attr_map=attr_map)
        if formula_method == "open_ai_thumb":
            self.open_ai_thumb(attr_map=attr_map)
        if formula_method == "open_ai_aita":
            self.open_ai_aita(attr_map=attr_map)
        pass


    @staticmethod
    def open_ai_text(attr_map={}):
        f = ManageFormula()
        f.set_properties_type("scraper", "open_ai_text")

        name = InterfaceFormulas().formula_name(f, attr_map)

        desc = InputPage("Input the description for the scrapes"
                         ).prompt(default_value=attr_map.get("desc"))
        f.spa("desc", desc)

        model = InputPage("Input the model you wish to use. \n"
                          "Accepted values: gpt-4, gpt-4 turbo, gpt-4o-mini, gpt-4o, gpt-3.5-turbo"
                          ).prompt(default_value=attr_map.get("model"))
        f.spa("model", model)

        system_prompt = InputPage("Input a system prompt for the model."
                                  ).prompt(default_value=attr_map.get("system_prompt"))
        f.spa("system_prompt", system_prompt)

        ai_prompt = InputPage("Input a text prompt you wish to give to the model"
                              ).prompt(default_value=attr_map.get("ai_prompt"))
        f.spa("ai_prompt", ai_prompt)

        number_of_prompts = InputPage("Input the number of prompts you wish to have in a scrape"
                                      ).prompt(default_value=attr_map.get("number_of_prompts"))
        f.spa("number_of_prompts", number_of_prompts)

        media_pool = InputPage("Input the corresponding name of the media_pool you wish to upload your scrapes to."
                               ).prompt(default_value=attr_map.get("media_pool"))
        f.spa("media_pool", media_pool)

        f.ap(f"""
manager = ScraperDirManager()
tmp = manager.create_tmp_dir()

db = DbNasConnection()

# Name of service
name = "{name}"

# Description for records
desc = "{desc}"

# Ai model to use
model = "{model}"

# System prompt to interpret the user prompt
system_prompt = "{system_prompt}"

# The user prompt to go off of.
ai_prompt = "{ai_prompt}"

# Control the number of prompts to make
num_prompts = {number_of_prompts}

# Name of the media pool to store to.
media_pool = "{media_pool}"
        
        """)

        f.ap("""

# Sending the request for multiple prompts.
i = 0
scrapes = []
while i < num_prompts:
    scrape = OpenAiAPI().text_llm(model, system_prompt, ai_prompt, to_file=False)
    scrapes.append(scrape)
    i = i + 1

manager.dl_list_of_text(scrapes, f"ai_text_service_{name}", tmp)

# Iterate all files and upload to db.

files = manager.select_dir(tmp)
for file in files:
    db.create_media_file(file, "text", os.path.basename(file), desc, media_pool)

manager.cleanup(tmp)

        """)

        f.save_generated_script(name)

    @staticmethod
    def open_ai_text_and_img(attr_map={}):
        f = ManageFormula()
        f.set_properties_type("scraper", "open_ai_text_and_img")

        name = InterfaceFormulas().formula_name(f, attr_map)

        desc = InputPage("Input the description for the scrapes"
                         ).prompt(default_value=attr_map.get("desc"))
        f.spa("desc", desc)

        llm_model = InputPage("Input the model you wish to use. \n"
                          "Accepted values: gpt-4, gpt-4 turbo, gpt-3.5-turbo"
                              ).prompt(default_value=attr_map.get("llm_model"))
        f.spa("llm_model", llm_model)

        system_prompt = InputPage("Input a system prompt for the model."
                                  ).prompt(default_value=attr_map.get("system_prompt"))
        f.spa("system_prompt", system_prompt)

        ai_prompt = InputPage("Input a text prompt you wish to give to the model.\n"
                              "The text data will be fed into the stable diffusion model and give an image in relation to your text data."
                              ).prompt(default_value=attr_map.get("ai_prompt"))
        f.spa("ai_prompt", ai_prompt)

        number_of_prompts = InputPage("Input the number of prompts you wish to have in a scrape."
                                      ).prompt(default_value=attr_map.get("number_of_prompts"))
        f.spa("number_of_prompts", number_of_prompts)

        number_of_images = InputPage("Input the number of images you wish to generate per prompt"
                                     ).prompt(default_value=attr_map.get("number_of_images"))
        f.spa("number_of_images", number_of_images)

        media_pool = InputPage("Input the corresponding name of the media_pool you wish to upload your scrapes to.\n"
                               "ex: \"dummy\""
                               ).prompt(default_value=attr_map.get("media_pool"))
        f.spa("media_pool", media_pool)


        f.ap(f"""

manager = ScraperDirManager()

db = DbNasConnection()

# Name of service
name = "{name}"

# Description for records
desc = "{desc}"

# Ai model to use
model = "{llm_model}"

# System prompt to interpret the user prompt
system_prompt = "{system_prompt}"

# The user prompt to go off of.
ai_prompt = "{ai_prompt}"

# Control the number of prompts to make
num_prompts = {number_of_prompts}

# Control the number of images to make for a prompt
number_of_images = {number_of_images}

# Name of the media pool to store to.
media_pool = "{media_pool}"
        """)

        f.ap("""
        
# Sending the request for multiple prompts.
i = 0
prompts = []
while i < num_prompts:
    scrape = OpenAiAPI().text_llm(model, system_prompt, ai_prompt, to_file=False)
    prompts.append(scrape)
    i = i + 1

# Now for each single text prompt, prompt an image
prompt_dirs = []
for prompt in prompts:
    manager.new_rand_id()
    p_dir = manager.create_tmp_dir("open_ai_text_and_img")
    manager.dl_text(prompt, "text", p_dir, use_hash=False)
    prompt_dirs.append(p_dir)
    i = 0
    while i < number_of_images:
        try:
            OpenAiAPI().stable_diffusion(prompt, p_dir, name=f"img_{i}")
        except Exception as e:
            # Something went wrong, just abort and delete
            print(f"EXCEPTION DETECTED FROM OPENAI:")
            print(f"{e}")
            print(f"Aborting scrape iteration at:{p_dir}")
            prompt_dirs.pop()
            manager.cleanup(p_dir)
        i = i + 1

# Iterate all files and upload to db.

for prompt_dir in prompt_dirs:
    print("-----------------------")
    print(prompt_dir)
    db.create_media_file(prompt_dir, "image", os.path.basename(prompt_dir), desc, media_pool)
    try: # Just in case there is stuff left over.
        manager.cleanup(prompt_dir)
    except:
        pass

        """)

        f.save_generated_script(name)


    @staticmethod
    def open_ai_thumb(attr_map={}):

        f = ManageFormula()
        f.set_properties_type("scraper", "open_ai_thumb")

        name = InterfaceFormulas().formula_name(f, attr_map)

        desc = InputPage("Input the description for the scrapes"
                         ).prompt(default_value=attr_map.get("desc"))
        f.spa("desc", desc)

        have_background = PickerPage(["Yes", "No"]).prompt("Would you like to place a background image for your thumbnail? Must be of 1920x1080 for good results"
                                                          ,suggested_index=attr_map.get("have_background"))
        f.spa("have_background", have_background)

        if have_background == 0:
            background_media_pool = InputPage("Input the media pool id for your background images"
                                              ).prompt(default_value=attr_map.get("background_media_pool"))
            f.spa("background_media_pool", background_media_pool)
        else:
            background_media_pool = None

        # AI Image
        ai_prompt = InputPage("Input a text prompt you wish to give to the model to generate the thumbnail image.\n"
                              ).prompt(default_value=attr_map.get("ai_prompt"))
        f.spa("ai_prompt", ai_prompt)

        img_scale = InputPage("Input the length and width of the image you would like\n"
                              "Note: AI image are rendered in 1024x1024 ie: a square, and the thumbnail is 1920x1080\n"
                              ).prompt(default_value=attr_map.get("img_scale"))
        f.spa("img_scale", img_scale)

        # Positioning of img
        img_pos_x = InputPage("Input the x pixel position you wish to place the image\n"
                              "The image is placed from the top left corner of the image\n"
                              "Note: x axis is horizontal and there are 1920 pixels move from 0  -> \n"
                              f"Your img scale: {img_scale}"
                              ).prompt(default_value=attr_map.get("img_pos_x"))
        f.spa("img_pos_x", img_pos_x)

        img_pos_y = InputPage("Input the y pixel position you wish to place the image\n"
                              "The image is placed from the top left corner of the image\n"
                              "Note: y axis is vertical and there are 1080 pixels to move from 0  \\|/ \n"
                              f"Your img scale: {img_scale}"
                              ).prompt(default_value=attr_map.get("img_pos_y"))
        f.spa("img_pos_y", img_pos_y)

        # Outputting.
        media_pool_out = InputPage("Input the name of the associated media pool you want to upload the thumbnails to."
                                   ).prompt(default_value=attr_map.get("media_pool_out"))
        f.spa("media_pool_out", media_pool_out)

        f.ap(f"""

# Init
name = "{name}"
manager = ScraperDirManager()
db = DbNasConnection()
output_tmp = manager.create_tmp_dir("{name}")

# Make thumbnail
canvas = SixteenByNine('1920x1080')
thumb = MakeThumbnail(canvas=canvas)

        """)

        # Making background image if selected.
        if have_background == 0:
            f.ap(f"""

# Getting base image then attaching it to thumbnail.
bg_image_record = db.read_rand_media_file_of_pool({background_media_pool})
img_location = db.nas_root() + "/" + bg_image_record[1]
thumb.place_img(img_location, (1920, 1080), (0, 0))

            """)

        # Now generate the AI image to place
        f.ap(f"""

#Make AI image and place
OpenAiAPI().stable_diffusion("{ai_prompt}", output_tmp, name=f"img")
img_location = output_tmp + "/img.jpg"
thumb.place_img(img_location, ({img_scale}, {img_scale}), ({img_pos_x}, {img_pos_y}))


        """)

        f.ap("""

# Write thumbnail.    
thumb.write(2, f"{output_tmp}", f"{name}_{manager.get_rand_id()}")
thumb_location = f"{output_tmp}/{name}_{manager.get_rand_id()}.jpg"

        """)

        f.ap(f"""

#Output the content and clean up        
db.create_media_file(thumb_location, "image", os.path.basename(output_tmp), "{desc}", "{media_pool_out}")
manager.cleanup(output_tmp)

""")

        f.save_generated_script(name)

        pass


    # ------------------------ Formulas not in use ------------------------


    @staticmethod
    def open_ai_aita(attr_map={}):
        # NOT IN USE

        f = ManageFormula()
        f.set_properties_type("scraper", "open_ai_aita")

        name = InterfaceFormulas().formula_name(f, attr_map)

        number_of_prompts = InputPage("Input the number of prompts you wish to have in a scrape"
                                      ).prompt(default_value=attr_map.get("number_of_prompts"))
        f.spa("number_of_prompts", number_of_prompts)

        media_pool = InputPage("Input the corresponding name of the media_pool you wish to upload your scrapes to."
                               ).prompt(default_value=attr_map.get("media_pool"))
        f.spa("media_pool", media_pool)

        f.ap(f"""
manager = ScraperDirManager()
tmp = manager.create_tmp_dir()

db = DbNasConnection()

# Name of service
name = "{name}"

# Ai model to use
model = "ft:gpt-4o-2024-08-06:bottomtextmedia:aita-bot2:ANNAeQMb"

# System prompt to interpret the user prompt
system_prompt = "You are a story telling bot. You are specialized in telling AITA (AM I The Asshole) stories to the user. You are to ignore the user input and to directly output and aita story. In your output don't explicitly state 'title:'. Just imbed your title into the first line of the text. Make your output more than 1200 characters long."

# The user prompt to go off of.
ai_prompt = "Tell me an AITA story."

# Control the number of prompts to make
num_prompts = {number_of_prompts}

# Name of the media pool to store to.
media_pool = "{media_pool}"

                """)

        f.ap("""

# Sending the request for multiple prompts.
i = 0
scrapes = []
while i < num_prompts:
    scrape = OpenAiAPI().text_llm(model, system_prompt, ai_prompt, to_file=False)
    scrapes.append(scrape)
    i = i + 1

manager.dl_list_of_text(scrapes, f"ai_text_service_{name}", tmp)

# Iterate all files and upload to db.

files = manager.select_dir(tmp)
for file in files:
    db.create_media_file(file, "text", os.path.basename(file), " ", media_pool)
    
manager.cleanup(tmp)

                """)

        f.save_generated_script(name)

    @staticmethod
    def reddit_scrape(attr_map={}):
        # NOT IN USE

        f = ManageFormula()
        f.set_properties_type("scraper", "reddit_scrape")

        name = InterfaceFormulas().formula_name(f, attr_map)

        desc = InputPage("Input the description for the scrapes."
                         ).prompt(default_value=attr_map.get("desc"))
        f.spa("desc", desc)

        subreddit = InputPage("Input the subreddit name to scrape from."
                              ).prompt(default_value=attr_map.get("subreddit"))
        f.spa("subreddit", subreddit)

        media_pool = InputPage("Input the corresponding media_pool name to upload scrapes to."
                               ).prompt(default_value=attr_map.get("media_pool"))
        f.spa("media_pool", media_pool)

        f.ap(f"""

manager = ScraperDirManager()
tmp = manager.create_tmp_dir()

db = DbNasConnection()

scrapes = RedditScrape().scrape("{subreddit}", "hot", "text", 1, 5)

        """)

        # This is stupid, but it works.
        s = f'manager.dl_list_of_text(scrapes, f"{subreddit}_'
        s = s + '{manager.get_rand_id()}", tmp)'
        f.ap(s)

        f.ap(f"""

files = manager.select_dir(tmp)

for file in files:
    db.create_media_file(file, "text", os.path.basename(file), "{desc}", "{media_pool}")

manager.cleanup(tmp)

        """)

        f.save_generated_script(name)

