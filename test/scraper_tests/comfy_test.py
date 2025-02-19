import json
from urllib import request, parse
import random

#This is the ComfyUI api prompt format.

#If you want it for a specific workflow you can "enable dev mode options"
#in the settings of the UI (gear beside the "Queue Size: ") this will enable
#a button on the UI to save workflows in api format.

#keep in mind ComfyUI is pre alpha software so this format will change a bit.

#this is the one for the default workflow
prompt_text = """
{
  "5": {
    "inputs": {
      "width": 1920,
      "height": 1080,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage"
  },
  "6": {
    "inputs": {
      "text": "A landscape image of an alien planet unlike earth. It is beautiful but I don't know how to describe it. It has lush grass but the color is atypical. The mountants are of weird shapes that make no sense yet all the sense in the world. And the sky, oh my the sky. It is nothing I have seen before. It is magic.",
      "clip": [
        "11",
        0
      ]
    },
    "class_type": "CLIPTextEncode"
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
    "class_type": "VAEDecode"
  },
  "9": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage"
  },
  "10": {
    "inputs": {
      "vae_name": "flux_ae.safetensors"
    },
    "class_type": "VAELoader"
  },
  "11": {
    "inputs": {
      "clip_name1": "t5xxl_fp8_e4m3fn.safetensors",
      "clip_name2": "t5xxl_fp8_e4m3fn.safetensors",
      "type": "sd3"
    },
    "class_type": "DualCLIPLoader"
  },
  "12": {
    "inputs": {
      "unet_name": "flux1-schnell.safetensors",
      "weight_dtype": "default"
    },
    "class_type": "UNETLoader"
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
    "class_type": "SamplerCustomAdvanced"
  },
  "16": {
    "inputs": {
      "sampler_name": "euler"
    },
    "class_type": "KSamplerSelect"
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
    "class_type": "BasicScheduler"
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
    "class_type": "BasicGuider"
  },
  "25": {
    "inputs": {
      "noise_seed": 407034628791774
    },
    "class_type": "RandomNoise"
  }
}
"""

def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req = request.Request("http://10.10.2.153:8188/prompt", data=data)
    request.urlopen(req)


prompt = json.loads(prompt_text)
# #set the text prompt for our positive CLIPTextEncode
# prompt["6"]["inputs"]["text"] = "masterpiece best quality man"
#
# #set the seed for our KSampler node
# prompt["3"]["inputs"]["seed"] = 5


queue_prompt(prompt)
