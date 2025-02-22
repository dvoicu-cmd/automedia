import json
import urllib
import uuid
import websocket
from urllib import request, parse
import time
import numpy as np
import cv2
import random

from lib.manage_directory_structure.scraper_dir_manager import ScraperDirManager


class ComfyUiAPI:
    def __init__(self, comfy_server_address, comfy_port=8188):
        self.comfy_address = comfy_server_address
        self.comfy_port = comfy_port
        self.sid = "0"
        self.noise_seed = random.randint(10 ** 14, 10 ** 15 - 1)
        self.comfy_workflow_dict = {}
        self.dm = ScraperDirManager()
        pass

    def __open_new_websocket_connection(self):
        """
        Opens a websocket
        :return: websocket object instance.
        """
        client_id = str(uuid.uuid4())
        ws = websocket.WebSocket()
        print(f"ws://{self.comfy_address}:{self.comfy_port}/ws?clientId={client_id}")
        ws.connect(f"ws://{self.comfy_address}:{self.comfy_port}/ws?clientId={client_id}")
        return ws


    def __track_progress(self, prompt_id):
        """
        Holds the process and tracks the current queue on the comfy server. Exits when there is nothing in queue or when the specified prompt finishes.
        :param prompt_id: integer that specifies the prompt to track.
        """
        # Open up new websocket connection
        ws = self.__open_new_websocket_connection()

        while True:
            out = ws.recv()  # receive messages
            if isinstance(out, str):
                message = json.loads(out)
                print(f"got message from comfy: \n{message}")

                # For status messages. This is for when the server has queued prompts
                # You want to break out of this websocket if the queue is 0
                if message['type'] == 'status':
                    # Get current queue count.
                    current_queue = message['data']['status']['exec_info']['queue_remaining']
                    if current_queue == 0:
                        print("nothing in queue, exit")
                        ws.close()
                        # Wait 5 seconds for history to load on the server.
                        time.sleep(5)
                        break

                # For in progress messages
                if message['type'] == 'progress':

                    msg_prompt_id = message['data']['prompt_id']
                    current_step = message['data']['value']
                    max_steps = message['data']['max']

                    print(f"given prompt id: {prompt_id}")
                    print(f"found prompt id: {msg_prompt_id}")
                    print(f"current step: {current_step}")
                    print(f"max step: {max_steps}")
                    print(f"given prompt id same as msg: {prompt_id == msg_prompt_id}")
                    print(f"current step greater than or equal to max step: {current_step >= max_steps}")

                    # When there have been enough steps for the specific prompt_id, exit this websocket.
                    if prompt_id == msg_prompt_id and current_step >= max_steps:
                        print("Finished processing.")
                        ws.close()
                        # Wait 5 seconds for history to load on the server.
                        time.sleep(5)
                        break

            else:
                continue
        return

    def __queue_prompt(self):
        """
        Queues a new prompt to the comfy server.
        :return: The prompt id of the newly queued prompt
        """
        prompt_json_format = json.dumps(self.comfy_workflow_dict, indent=4).encode('utf-8')
        req = request.Request(f"http://{self.comfy_address}:{self.comfy_port}/prompt", data=prompt_json_format)

        with request.urlopen(req) as response:
            response_data = response.read().decode("utf-8")  # Read and decode response
            response_json = json.loads(response_data)  # Parse JSON

            if "prompt_id" in response_json:
                return response_json["prompt_id"]  # Extract "prompt_id"

        return None  # Return None if "prompt_id" isn't found

    def __get_history(self, prompt_id):
        """
        Gets the history details of a specific prompt on the comfy server. For getting the file name to get.
        :param prompt_id:
        :return:
        """
        req = request.Request(f"http://{self.comfy_address}:{self.comfy_port}/history/{prompt_id}")
        with request.urlopen(req) as response:
            response_data = response.read().decode("utf-8")  # Read and decode response
            json_history = json.loads(response_data)  # Parsed JSON
            return json_history

    @staticmethod
    def __get_image_paths(prompt_id, json_history):
        """
        Gets the image path on the comfy server given an id and json_history
        :param prompt_id: The prompt id
        :param json_history: The json details returned from __get_history()
        :return: An array of two containing the filename and the subdirectory values of the specific prompt.
        """

        # Get the specific json section with the output name data on the server.
        outputs = json_history[prompt_id]["outputs"]["9"]["images"]
        image_map = []
        for item in outputs:
            filename = item["filename"]
            subfolder = item["subfolder"]
            image_map.append([filename, subfolder])
        return image_map

    def __save_images(self, prompt_id, image_map, path_dir_output):
        """
        Saves the prompts
        :param prompt_id: The prompt id used for naming the output file
        :param image_map: The image map returned from the __get_image_paths() method.
        :param path_dir_output: The location you want to save the image(s) to.
        """

        random_string = self.dm.generate_random_string(5)

        got_images = []

        for specific_map in image_map:
            # map[0] -> The filename, map[1] -> the subfolder
            req = request.Request(f"http://{self.comfy_address}:{self.comfy_port}/view?filename={specific_map[0]}&subfolder={specific_map[1]}")
            with request.urlopen(req) as response:
                response_data = response.read()  # Read binary image data
                np_array = np.frombuffer(response_data, np.uint8)  # Convert to NumPy array
                image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)  # Decode image using OpenCV
                got_images.append(image)

        i = 0
        for image in got_images:
            filename = f"comfyUI_id?{prompt_id[:10]}_batch?{i}_{random_string}.png"
            absolute_path_to_write = f"{path_dir_output}/{filename}"
            cv2.imwrite(absolute_path_to_write, image)
            i += 1



    def stable_diffusion(self, path_dir_output=''):
        """
        Prompts the comfyui server and saves the generated images with the specified parameters
        :param path_dir_output: The specific path to save the image(s)
        :return:
        """

        if not self.comfy_workflow_dict:
            raise AttributeError("Prompt has not been specified.")

        print("queue prompt")
        prompt_id = self.__queue_prompt()
        print(f"Prompt ID: {prompt_id}")

        print("tracking progress of prompt")
        self.__track_progress(prompt_id)

        print("getting prompt history")
        history = self.__get_history(prompt_id)

        print("getting images")
        img_maps = self.__get_image_paths(prompt_id, history)
        self.__save_images(prompt_id, img_maps, path_dir_output)

    def set_prompt(self, width, height, batch_size, prompt_text):
        """
        Specifies the prompt parameters to send to comfyui server.
        :param width: The width of the image to generate
        :param height: The height of the image to generate
        :param batch_size: How many images to generate in one go.
        :param prompt_text: The text input for the prompt.
        :return:
        """
        self.comfy_workflow_dict = {
            "prompt":
            {
                "5": {
                    "inputs": {
                    "width": width,
                    "height": height,
                    "batch_size": batch_size
                    },
                    "class_type": "EmptyLatentImage",
                    "_meta": {
                    "title": "Empty Latent Image"
                    }
                },
                "6": {
                    "inputs": {
                    "text": prompt_text,
                    "clip": [
                        "11",
                        0
                    ]
                    },
                    "class_type": "CLIPTextEncode",
                    "_meta": {
                    "title": "CLIP Text Encode (Prompt)"
                    }
                },
                "8": {
                    "inputs": {
                    "samples": [
                        "13",
                        0
                    ],
                    "vae": [
                        "10",
                        0
                    ]
                    },
                    "class_type": "VAEDecode",
                    "_meta": {
                    "title": "VAE Decode"
                    }
                },
                "9": {
                    "inputs": {
                    "filename_prefix": "ComfyUI",
                    "images": [
                        "8",
                        0
                    ]
                    },
                    "class_type": "SaveImage",
                    "_meta": {
                    "title": "Save Image"
                    }
                },
                "10": {
                    "inputs": {
                    "vae_name": "flux_ae.safetensors"
                    },
                    "class_type": "VAELoader",
                    "_meta": {
                    "title": "Load VAE"
                    }
                },
                "11": {
                    "inputs": {
                    "clip_name1": "t5xxl_fp8_e4m3fn.safetensors",
                    "clip_name2": "t5xxl_fp8_e4m3fn.safetensors",
                    "type": "sd3"
                    },
                    "class_type": "DualCLIPLoader",
                    "_meta": {
                    "title": "DualCLIPLoader"
                    }
                },
                "12": {
                    "inputs": {
                    "unet_name": "flux1-schnell.safetensors",
                    "weight_dtype": "fp8_e4m3fn_fast"
                    },
                    "class_type": "UNETLoader",
                    "_meta": {
                    "title": "Load Diffusion Model"
                    }
                },
                "13": {
                    "inputs": {
                    "noise": [
                        "25",
                        0
                    ],
                    "guider": [
                        "22",
                        0
                    ],
                    "sampler": [
                        "16",
                        0
                    ],
                    "sigmas": [
                        "17",
                        0
                    ],
                    "latent_image": [
                        "5",
                        0
                    ]
                    },
                    "class_type": "SamplerCustomAdvanced",
                    "_meta": {
                    "title": "SamplerCustomAdvanced"
                    }
                },
                "16": {
                    "inputs": {
                    "sampler_name": "euler"
                    },
                    "class_type": "KSamplerSelect",
                    "_meta": {
                    "title": "KSamplerSelect"
                    }
                },
                "17": {
                    "inputs": {
                    "scheduler": "simple",
                    "steps": 4,
                    "denoise": 1,
                    "model": [
                        "12",
                        0
                    ]
                    },
                    "class_type": "BasicScheduler",
                    "_meta": {
                    "title": "BasicScheduler"
                    }
                },
                "22": {
                    "inputs": {
                    "model": [
                        "12",
                        0
                    ],
                    "conditioning": [
                        "6",
                        0
                    ]
                    },
                    "class_type": "BasicGuider",
                    "_meta": {
                    "title": "BasicGuider"
                    }
                },
                "25": {
                    "inputs": {
                    "noise_seed": self.noise_seed
                    },
                    "class_type": "RandomNoise",
                    "_meta": {
                    "title": "RandomNoise"
                    }
                }
            }
        }
        # You want to then create a new random seed.
        self.noise_seed = random.randint(10 ** 14, 10 ** 15 - 1)
