# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: content_retrieval.py
# @time: 2024/4/2 16:42
import os
import json

from pymilvus import MilvusClient

from get_mm_embedding import get_multi_modal_embedding
from get_mm_embedding import get_text_embedding


class ContentRetrieval(object):
    def __init__(self, query, milvus_client):
        self.query = query
        self.milvus_client = milvus_client
        self.image_limit_number = 10

    def image_retrieval_by_embedding(self):
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
            output_fields=['text', 'page_no', 'pdf_path']
        )
        result = [_['entity'] for _ in res[0]]
        pdf_page_no_dict = {}
        for record in result:
            pdf_path = record['pdf_path']
            if pdf_path not in pdf_page_no_dict:
                pdf_page_no_dict[pdf_path] = [record['page_no']]
            else:
                if record['page_no'] not in pdf_page_no_dict[pdf_path]:
                    pdf_page_no_dict[pdf_path].append(record['page_no'])
        return pdf_page_no_dict, result

    @staticmethod
    def image_retrieval_by_text_page(pdf_page_no_dict: dict):
        additional_image_list = []
        for pdf_path, page_no_set in pdf_page_no_dict.items():
            file_name = os.path.basename(pdf_path).split('.')[0]
            output_dir = f"../output/{file_name}"
            with open(os.path.join(output_dir, "table_figure_caption.json"), "r") as f:
                table_figure_caption_dict = json.loads(f.read())
            for page_no in page_no_set:
                for file in os.listdir(output_dir):
                    image_path = os.path.join(output_dir, file)
                    if file.startswith('[') and f']_{page_no}.jpg' in file:
                        additional_image_list.append({'data_type': 'image',
                                                      'image_path': image_path,
                                                      'text': table_figure_caption_dict.get(file, "")})
                    elif "table" in file and file.startswith(str(page_no)):
                        additional_image_list.append({'data_type': 'table',
                                                      'image_path': image_path,
                                                      'text': table_figure_caption_dict.get(file, "")})

        return additional_image_list

    def run(self):
        image_embedding_result = self.image_retrieval_by_embedding()
        pdf_page_no_dict, text_result = self.text_retrieval()
        image_additional_result = self.image_retrieval_by_text_page(pdf_page_no_dict)
        # 图片去重并限制数量
        for img_item in image_additional_result:
            if img_item not in image_embedding_result and len(image_embedding_result) < self.image_limit_number:
                image_embedding_result.append(img_item)
        image_result = image_embedding_result[:self.image_limit_number]
        print(text_result)
        print(pdf_page_no_dict)
        print(json.dumps(image_result))
        return image_result, text_result


if __name__ == '__main__':
    client = MilvusClient(uri="http://localhost:19530", db_name="default")
    # my_query = "What is LLaMA-7B's zero-shot accuracy on RACE dataset?"
    # my_query = "What is LLaMA model's accuracy on MMLU dataset?"
    # my_query = "LLaMA zero-shot performance on PIQA, SIQA, BoolQ dataset"
    # my_query = "pretraining data of LLaMA and their prop"
    my_query = "What is the training framework of BLOOM? What's the number of data parallelism, tensor parallelism, pipeline parallelism in 3D-parallelism during the training of BLOOM?"
    content_retriever = ContentRetrieval(query=my_query, milvus_client=client)
    content_retriever.run()
    client.close()
