import os
import sys

from lib.manage_formula.manage_formula import ManageFormula
from lib.cli_interface.input_pages import InputPage
from lib.cli_interface.picker_pages import PickerPage


class ScraperFormulas:
    def __init__(self):
        pass

    @staticmethod
    def reddit_scrape():
        f = ManageFormula()
        name = InputPage("Input the name of the service").prompt()
        desc = InputPage("Input the description for the scrapes").prompt()
        subreddit = InputPage("Input the subreddit name").prompt()
        media_pool = InputPage("Input the corresponding media_pool").prompt()

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
        print(200)

    @staticmethod
    def open_ai_text():
        f = ManageFormula()
        name = InputPage("Input the name of the service").prompt()
        desc = InputPage("Input the description for the scrapes").prompt()
        model = InputPage("Input the model you wish to use. \n"
                          "Accepted values: gpt-4, gpt-4 turbo, gpt-3.5-turbo").prompt()
        system_prompt = InputPage("Input a system prompt for the model.")
        ai_prompt = InputPage("Input a text prompt you wish to give to the model").prompt()
        number_of_prompts = InputPage("Input the number of prompts you wish to have in a scrape").prompt()
        media_pool = InputPage("Input the corresponding media_pool").prompt()

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
media_pool = {media_pool}
        
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
        print(200)

    @staticmethod
    def open_ai_text_and_img():
        f = ManageFormula()
        name = InputPage("Input the name of the service").prompt()
        desc = InputPage("Input the description for the scrapes").prompt()
        llm_model = InputPage("Input the model you wish to use. \n"
                          "Accepted values: gpt-4, gpt-4 turbo, gpt-3.5-turbo").prompt()
        system_prompt = InputPage("Input a system prompt for the model.").prompt()
        ai_prompt = InputPage("Input a text prompt you wish to give to the model.\n"
                              "The text data will be fed into the stable diffusion model and give an image in relation to your text data.").prompt()
        number_of_prompts = InputPage("Input the number of prompts you wish to have in a scrape").prompt()
        number_of_images = InputPage("Input the number of images you wish to generate per prompt").prompt()
        media_pool = InputPage("Input the corresponding name of the media_pool you wish to upload your scrapes to.\n"
                               "ex: \"dummy\"").prompt()

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
        print(200)



