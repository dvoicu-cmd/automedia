import json
import urllib
import uuid
import websocket
from urllib import request, parse
import time

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
            "batch_size": 1
            },
            "class_type": "EmptyLatentImage",
            "_meta": {
            "title": "Empty Latent Image"
            }
        },
        "6": {
            "inputs": {
            "text": "JSON.",
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

    def __get_history(self, prompt_id):
        req = request.Request(f"{self.comfy_address}/history/{prompt_id}")
        with request.urlopen(req) as response:
            response_data = response.read().decode("utf-8")  # Read and decode response
            response_json = json.loads(response_data)  # Parsed JSON
            return response_json


    def __track_progress(self, prompt_json, prompt_id):
        ws = self.__open_new_websocket_connection()

        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                print(f"recived message from comfy: {message}")

                # For status messages. This is for when the server has queued prompts
                # You want to break out of this websocket if the queue is 0
                if message['type'] == 'status':
                    print(message['data']['status']['exec_info']['queue_remaining'])
                    # # data = json.loads(message['data'])
                    # print(f"message data: {data}")

                #
                # if message['type'] == 'progress':
                #
                #     try:
                #         data = message['data']
                #         current_step = data['value']
                #         final_step = data['max']
                #         message_prompt_id = message['prompt_id']
                #
                #         print(data)
                #         print(current_step)
                #         print(final_step)
                #         print(message_prompt_id)
                #
                #         if current_step >= final_step:
                #             print(f"finished execution of prompt:{prompt_id}")
                #             time.sleep(10)
                #             break  # Execution is done
                #
                #     except KeyError as e:
                #         print("Errr err errrrrrrrrr fuck")
                #         print(e)
                #         continue

                # print('In K-Sampler -> Step: ', current_step, ' of: ', data['max'])

                # if message['type'] == 'execution_cached':
                #     data = message['data']
                #     for itm in data['nodes']:
                #         if itm not in finished_nodes:
                #             finished_nodes.append(itm)
                #             print('Progess: ', len(finished_nodes), '/', len(node_ids), ' Tasks done')
                # if message['type'] == 'executing':
                #     data = message['data']
                #     if data['node'] not in finished_nodes:
                #         finished_nodes.append(data['node'])
                #         print('Progess: ', len(finished_nodes), '/', len(node_ids), ' Tasks done')
                # if data['node'] is None and data['prompt_id'] == prompt_id:
                #         break #Execution is done

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
        self.__track_progress(self.prompt_json_format, prompt_id)

        print("getting prompt history")
        result = self.__get_history(prompt_id)
        print(f"Result json \n {prompt_id}")

        pass
