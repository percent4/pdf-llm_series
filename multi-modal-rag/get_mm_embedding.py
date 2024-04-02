# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: get_mm_embedding.py
# @time: 2024/4/2 16:03
# 获取图片和表格的多模态embedding
import json
import base64
import os
import fitz
from dotenv import load_dotenv

import requests
from pymilvus import MilvusClient
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()


def get_image_base64_str(image_path):
    with open(image_path, "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode('utf-8')
    return data


def get_multi_modal_embedding(image_path=None, text=""):
    if image_path is not None:
        with open(image_path, "rb") as image_file:
            data = base64.b64encode(image_file.read()).decode('utf-8')
    else:
        data = ""

    url = "http://35.89.147.116:50074/mm_embedding"
    payload = json.dumps({
        "image_base64": data, "text": text
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()['embedding']


def get_text_embedding(text_chunks):
    url = "https://api.openai.com/v1/embeddings"
    payload = json.dumps({
        "model": "text-embedding-ada-002",
        "input": text_chunks,
        "encoding_format": "float"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    embedding = [_["embedding"] for _ in response.json()['data']]
    response.close()
    return embedding


class ImageEmbedding(object):
    def __init__(self, pdf_file_path, res_dir, milvus_client):
        self.res_dir = res_dir
        self.pdf_file_path = pdf_file_path
        self.milvus_client = milvus_client

    def run(self):
        with open(os.path.join(self.res_dir, "table_figure_caption.json"), "r") as f:
            table_figure_caption_dict = json.loads(f.read())

        entities = []
        _id = 1
        for file in os.listdir(self.res_dir):
            if (file.startswith('[') or file.startswith('table')) and file.endswith('jpg'):
                file_path = os.path.join(self.res_dir, file)
                caption = table_figure_caption_dict.get(file, "")
                print(f'get embedding for {file_path} with caption: {caption}')
                image_embedding = get_multi_modal_embedding(image_path=file_path, text=caption)
                data_type = "table" if "table" in file else "image"
                entities.append({"id": _id, "pdf_path": self.pdf_file_path, "data_type": data_type, "text": caption,
                                 "image_path": file_path, "embedding": image_embedding})
                _id += 1

        # Inserts vectors in the collection
        self.milvus_client.insert(collection_name="pdf_image_qa", data=entities)


class TextEmbedding(object):
    def __init__(self, pdf_file_path, milvus_client):
        self.pdf_file_path = pdf_file_path
        self.milvus_client = milvus_client

    def get_texts(self):
        text_list = []
        doc = fitz.open(self.pdf_file_path)
        page_number = doc.page_count
        for i in range(page_number):
            page = doc[i]
            text_list.append(page.get_text())
        doc.close()
        return text_list

    @staticmethod
    def get_chunks(text_list):
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=300, chunk_overlap=0, encoding_name="cl100k_base"
        )
        chunks = []
        for text in text_list:
            chunks.extend(text_splitter.split_text(text))
        return chunks

    def run(self):
        text_list = self.get_texts()
        chunks = self.get_chunks(text_list=text_list)
        batch_size = 10
        start_no = 0
        chunk_embeddings = []
        while start_no < len(chunks):
            print(f"start no: {start_no}")
            batch_chunk_embeddings = get_text_embedding(text_chunks=chunks[start_no:start_no+batch_size])
            chunk_embeddings.extend(batch_chunk_embeddings)
            start_no += batch_size
        entities = [{"id": i+1, "pdf_path": self.pdf_file_path, "text": chunks[i], "embedding": chunk_embeddings[i]}
                    for i in range(len(chunks))]
        self.milvus_client.insert(collection_name="pdf_text_qa", data=entities)


if __name__ == '__main__':
    pdf_path = '../data/LLaMA.pdf'
    res_output_dir = '../output/LLaMA'
    client = MilvusClient(uri="http://localhost:19530", db_name="default")
    my_image_embedding = ImageEmbedding(pdf_file_path=pdf_path, res_dir=res_output_dir, milvus_client=client)
    my_image_embedding.run()
    text_embedding = TextEmbedding(pdf_file_path=pdf_path, milvus_client=client)
    text_embedding.run()
    client.close()
