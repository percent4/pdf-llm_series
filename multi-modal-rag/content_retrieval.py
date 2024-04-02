# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: content_retrieval.py
# @time: 2024/4/2 16:42
from pymilvus import MilvusClient

from get_mm_embedding import get_multi_modal_embedding
from get_mm_embedding import get_text_embedding


class ContentRetrieval(object):
    def __init__(self, query, milvus_client):
        self.query = query
        self.milvus_client = milvus_client

    def image_retrieval(self):
        query_embedding = get_multi_modal_embedding(text=self.query)
        res = self.milvus_client.search(
            collection_name="pdf_image_qa",
            data=[query_embedding],
            limit=5,
            search_params={"metric_type": "IP", "params": {}},
            output_fields=['data_type', 'text', 'image_path']
        )
        return [_['entity'] for _ in res[0]]

    def text_retrieval(self):
        query_text_embedding = get_text_embedding(text_chunks=[self.query])
        res = self.milvus_client.search(
            collection_name="pdf_text_qa",
            data=query_text_embedding,
            limit=10,
            search_params={"metric_type": "IP", "params": {}},
            output_fields=['text']
        )
        return [_['entity'] for _ in res[0]]

    def run(self):
        image_result = self.image_retrieval()
        text_result = self.text_retrieval()
        return image_result, text_result


if __name__ == '__main__':
    client = MilvusClient(uri="http://localhost:19530", db_name="default")
    my_query = "What is LLaMA-7B's zero-shot accuracy on RACE dataset?"
    # my_query = "What is LLaMA model's accuracy on MMLU dataset?"
    # my_query = "LLaMA zero-shot performance on PIQA, SIQA, BoolQ dataset"
    # my_query = "pretraining data of LLaMA and their prop"
    content_retriever = ContentRetrieval(query=my_query, milvus_client=client)
    content_retriever.run()
    client.close()
