# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: deepl_translation.py
# @time: 2024/3/22 15:42
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()


def translate_api(text):
    url = "https://api.deepl.com/v2/translate"
    payload = json.dumps({
        "text": [
            text
        ],
        "target_lang": "ZH"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'DeepL-Auth-Key {os.getenv("DEEPL_API_KEY")}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()["translations"][0]["text"]
