# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: bge_v_embedding_server.py
# @time: 2024/4/2 21:50
import torch
from FlagEmbedding.visual.modeling import Visualized_BGE
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import base64
from PIL import Image
from io import BytesIO

app = FastAPI()


class MultiModal(BaseModel):
    image_base64: str = ""
    text: str = ""

model = Visualized_BGE(model_name_bge = "BAAI/bge-m3", model_weight="/data-ai/usr/lmj/models/bge-visualized/Visualized_m3.pth")
model.eval()
print("model loaded!")


@app.get('/')
def home():
    return 'hello world'


@app.post('/mm_embedding')
def get_mm_embedding(multi_modal: MultiModal):
    if multi_modal.image_base64:
        with Image.open(BytesIO(base64.b64decode(multi_modal.image_base64))) as im:
            image_path = 'tmp.png'
            im.save(image_path, 'PNG')
        with torch.no_grad():
            query_emb = model.encode(image=image_path, text=multi_modal.text)
    else:
        with torch.no_grad():
            query_emb = model.encode(text=multi_modal.text)
    print(query_emb)
    return {"embedding": query_emb.tolist()[0]}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=50074)
