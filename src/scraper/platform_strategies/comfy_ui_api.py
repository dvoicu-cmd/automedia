import json
import urllib
import uuid
import websocket
from urllib import request, parse
import time
import numpy as np
import cv2

from lib.manage_directory_structure.scraper_dir_manager import  ScraperDirManager


class ComfyUiAPI:
    def __init__(self):

        self.comfy_address = "ollama-host:8188"
        self.sid = "0"
        self.prompt_json_format = '''
{
    "prompt": 
    {
        "5": {
            "inputs": {
            "width": 200,
            "height": 200,
            "batch_size": 2
            },
            "class_type": "EmptyLatentImage",
            "_meta": {
            "title": "Empty Latent Image"
            }
        },
        "6": {
            "inputs": {
            "text": "man falling down stairs. The electric boogalu",
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
            "noise_seed": 698610413302783
            },
            "class_type": "RandomNoise",
            "_meta": {
            "title": "RandomNoise"
            }
        }
    }
}
'''

        pass


    def __open_new_websocket_connection(self):
        client_id = str(uuid.uuid4())
        ws = websocket.WebSocket()
        print(f"ws://{self.comfy_address}/ws?clientId={client_id}")
        ws.connect(f"ws://{self.comfy_address}/ws?clientId={client_id}")
        return ws


    def __track_progress(self, prompt_id):
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
                        break

                # For in progress messages
                if message['type'] == 'progress':

                    msg_prompt_id = message['data']['prompt_id']
                    current_step = message['data']['value']
                    max_steps = message['data']['max']

                    # When there have been enough steps for the specific prompt_id, exit this websocket.
                    if prompt_id == msg_prompt_id and current_step >= max_steps:
                        print("Finished processing")
                        ws.close()
                        break

            else:
                continue
        return

    def __queue_prompt(self, prompt_json):
        """
        Queues the stable diffusion prompt to be processed.
        :param prompt:
        :return:
        """

        prompt_dict = json.loads(prompt_json)
        data = json.dumps(prompt_dict).encode('utf-8')
        req = request.Request(f"http://{self.comfy_address}/prompt", data=data)

        with request.urlopen(req) as response:
            response_data = response.read().decode("utf-8")  # Read and decode response
            response_json = json.loads(response_data)  # Parse JSON

            if "prompt_id" in response_json:
                return response_json["prompt_id"]  # Extract "prompt_id"

        return None  # Return None if "prompt_id" isn't found

    def __get_history(self, prompt_id):
        req = request.Request(f"http://{self.comfy_address}/history/{prompt_id}")
        with request.urlopen(req) as response:
            response_data = response.read().decode("utf-8")  # Read and decode response
            json_history = json.loads(response_data)  # Parsed JSON
            return json_history

    def __get_image_paths(self, prompt_id, json_history):
        # print(json_history[prompt_id]["outputs"])
        # Get the specific json section with the output name data on the server.
        outputs = json_history[prompt_id]["outputs"]["9"]["images"]
        image_map = []
        for item in outputs:
            filename = item["filename"]
            subfolder = item["subfolder"]

            image_map.append([filename, subfolder])

        return image_map

    def __get_images(self, image_map):
        got_images = []

        for specific_map in image_map:
            #http://ollama-host:8188/view?filename=ComfyUI_00031_.png
            # map[0] -> The filename, map[1] -> the subfolder
            req = request.Request(f"http://{self.comfy_address}/view?filename={specific_map[0]}&subfolder={specific_map[1]}")
            with request.urlopen(req) as response:
                response_data = response.read()  # Read binary image data
                np_array = np.frombuffer(response_data, np.uint8)  # Convert to NumPy array
                image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)  # Decode image using OpenCV
                got_images.append(image)

        i = 0
        for image in got_images:
            filename = f"dl_{i}.png"
            cv2.imwrite(filename, image)  # SAVES THE IMAGE. LETS GO
            i += 1



    def stable_diffusion(self, prompt, path_dir_output='', name=None):
        """

        :param prompt:
        :param path_dir_output:
        :param name:
        :return:
        """

        print("queue prompt")
        prompt_id = self.__queue_prompt(self.prompt_json_format)
        print(f"Prompt ID: {prompt_id}")

        print("tracking progress of prompt")
        self.__track_progress(self.prompt_json_format)

        print("getting prompt history")
        history = self.__get_history(prompt_id)
        print(f"Result json \n {history}")

        print("getting image maps")
        img_maps = self.__get_image_paths(prompt_id, history)

        images = self.__get_images(image_map=img_maps)

        print(images)

        pass
