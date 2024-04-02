# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: vector_db_schema.py
# @time: 2024/3/28 15:02
import time
from pymilvus import MilvusClient, FieldSchema, CollectionSchema, DataType

image_collection_name = "pdf_image_qa"
text_collection_name = "pdf_text_qa"
# Connects to a server
client = MilvusClient(uri="http://localhost:19530", db_name="default")


def create_schema(collect_name, fields, desc):
    schema = CollectionSchema(fields, description=desc)
    index_params = client.prepare_index_params()
    index_params.add_index(
        field_name="embedding",
        index_type="IVF_FLAT",
        metric_type="IP",
        params={"nlist": 128}
    )
    client.create_collection(
        collection_name=collect_name,
        schema=schema,
        index_params=index_params
    )
    time.sleep(3)
    res = client.get_load_state(
        collection_name=collect_name
    )
    print("load state: ", res)


if not client.has_collection(image_collection_name) and not client.has_collection(text_collection_name):
    # Creates an image collection
    images_fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="pdf_path", dtype=DataType.VARCHAR, max_length=100),
        FieldSchema(name="data_type", dtype=DataType.VARCHAR, max_length=20),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=1000),
        FieldSchema(name="image_path", dtype=DataType.VARCHAR, max_length=300),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1024)
    ]
    image_collection_desc = "image embedding for pdf file"
    create_schema(collect_name=image_collection_name, fields=images_fields, desc=image_collection_desc)
    # Creates a text collection
    text_fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="pdf_path", dtype=DataType.VARCHAR, max_length=100),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=3000),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536)
    ]
    text_collection_desc = "text embedding for pdf file"
    create_schema(collect_name=text_collection_name, fields=text_fields, desc=text_collection_desc)

client.close()
