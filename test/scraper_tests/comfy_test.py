from context import src

import json
import urllib
import uuid
import websocket
from urllib import request, parse
import time

import random
from src.scraper.platform_strategies.comfy_ui_api import ComfyUiAPI

#This is the ComfyUI api prompt format.

#If you want it for a specific workflow you can "enable dev mode options"
#in the settings of the UI (gear beside the "Queue Size: ") this will enable
#a button on the UI to save workflows in api format.

#keep in mind ComfyUI is pre alpha software so this format will change a bit.

#this is the one for the default workflow

# Note that asking for the same text response, will give the exact same image.
prompt_text = """
{
  "5": {
    "inputs": {
      "width": 200,
      "height": 200,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage"
  },
  "6": {
    "inputs": {
      "text": "more gun",
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


comfy = ComfyUiAPI("ollama-host")
comfy.set_prompt(512, 512, 2, "Yeah.")
comfy.stable_diffusion()


