# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: mm_doc_qa.py
# @time: 2024/4/2 17:01
import json
import os
import base64

import requests
from dotenv import load_dotenv
from pymilvus import MilvusClient

from content_retrieval import ContentRetrieval


load_dotenv()


class MultiModelQA(object):
    def __init__(
        self,
        query: str,
        text_chunks: list[str],
        images: list[str],
        captions: list[str],
    ):
        self.query = query
        self.images = images
        self.text_chunks = text_chunks
        self.captions = captions

    @staticmethod
    def encode_image(image_path: str):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def make_prompt(self):
        # Getting the base64 string
        image_content = [
            {
                "type": "text",
                "text": self.query
            },
        ]
        for image in self.images:
            base64_image = self.encode_image(image)
            image_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })
        # get caption desc
        seq_no_list = ['first', 'second', 'third', 'forth', 'fifth']
        caption_list = []
        for i, caption in enumerate(self.captions):
            caption_list.append(
                f"The caption of {seq_no_list[i]} image is {caption}.")
        caption_desc = '\n'.join(caption_list)
        messages = [{"role": "system",
                     "content": "You are a helpful assistant."},
                    {"role": "user",
                     "content": f"<Text from PDF file>:\n\n{''.join(self.text_chunks)}"},
                    {"role": "user",
                     "content": caption_desc},
                    {"role": "user",
                     "content": image_content}]
        # print(json.dumps(messages, ensure_ascii=False))
        return messages

    @staticmethod
    def make_request(messages):
        # make request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
        }
        payload = {"model": "gpt-4-vision-preview",
                   "messages": messages,
                   "max_tokens": 500}

        response = requests.post(
            url="https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload)

        return response.json()['choices'][0]['message']['content']

    def run(self):
        messages = self.make_prompt()
        answer = self.make_request(messages=messages)
        return answer


if __name__ == '__main__':
    client = MilvusClient(uri="http://localhost:19530", db_name="default")
    my_query = "What is LLaMA-7B's zero-shot accuracy on RACE dataset?"
    my_query = "What is LLaMA model's average accuracy on MMLU dataset?"
    # my_query = "LLaMA 7B zero-shot performance on PIQA, SIQA, BoolQ dataset"
    my_query = "pretraining data of LLaMA and their prop"
    # my_query = "What are mathematical reasoning benchmarks in this paper?"
    # my_query = "what is the use of TruthfulQA?"
    my_query = "What's carbon emission of BLOOM?"
    my_query = "What's the number of data parallelism, tensor parallelism, pipeline parallelism in 3D-parallelism during the training of BLOOM?"
    my_query = "what is the training framework of BLOOM?"
    content_retriever = ContentRetrieval(query=my_query, milvus_client=client)
    image_result, text_result = content_retriever.run()
    retrieved_text_chunks = [_['text'] for _ in text_result]
    retrieved_images = [_['image_path'] for _ in image_result]
    print(retrieved_images)
    retrieved_captions = [_['text'] for _ in image_result]
    print(retrieved_captions)
    mm_qa = MultiModelQA(
        query=my_query,
        text_chunks=retrieved_text_chunks,
        images=retrieved_images,
        captions=retrieved_captions)
    doc_answer = mm_qa.run()
    print(doc_answer)
    client.close()
