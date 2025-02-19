import pdb
import requests
import json

from lib.manage_directory_structure.scraper_dir_manager import  ScraperDirManager

class OllamaAPI:
    def __init__(self, host_name):
        self.dm = ScraperDirManager()
        self.url = "http://"+host_name+":11434/api/generate"

    def text_llm(self, model, system_msg, user_msg, to_file=True, path_dir_output=''):

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "model": f"{model}",  # Replace with an actual model on your machine
            "system": f"{system_msg}",
            "prompt": f"{user_msg}",
            "stream": True  # Ensures a full response instead of streamed output
        }

        # Send in request and parse the chunks
        response = requests.post(url=self.url, json=payload, headers=headers, stream=True)
        messages = []  # The list of json responses from each chunk
        message = ""  # tmp string that builds the json response.
        for chunk in response.iter_content():
            if chunk:
                decoded = chunk.decode("utf-8")
                if "}" in message:  # If you see a close, that is the end of the specific chunk.
                    message = message + decoded
                    messages.append(message)
                    message = ""
                else:
                    message = message + decoded

        # parse the raw strings to json and get the response data.
        llm_response = ""
        for message in messages:
            data = json.loads(message)
            if "response" in data:
                llm_response += data["response"]

        if to_file:
            self.dm.dl_text(llm_response, f"llm_txt_{user_msg[:10]}", path_dir_output)
            return None
        else:
            return llm_response




