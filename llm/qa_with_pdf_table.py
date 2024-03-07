# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: qa_with_pdf_table.py
# @time: 2024/3/7 14:20
import os
import fitz
import base64
import requests
from pprint import pprint


def get_pdf_content(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    num_pages = doc.page_count
    bg_content_list = []

    # Full Text of PDF
    for page_index in range(num_pages):
        page = doc.load_page(page_index)
        text = page.get_text()
        bg_content_list.append(text)

    return ''.join(bg_content_list)


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def make_request(pdf_content, images, query):
    # Getting the base64 string
    image_content = [
        {
            "type": "text",
            "text": query
        },
    ]
    for image in images:
        base64_image = encode_image(image)
        image_content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })
    # OpenAI API Key
    api_key = os.getenv("OPENAI_API_KEY")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {"model": "gpt-4-vision-preview",
               "messages": [{"role": "system",
                             "content": "You are a helpful assistant."},
                            {"role": "user",
                             "content": f"The full text of PDF file is: {pdf_content}"},
                            {"role": "user",
                             "content": image_content}],
               "max_tokens": 300}

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload)

    pprint(response.json()['choices'])


if __name__ == '__main__':
    pdf_file_path = '../data/demo2.pdf'
    table_images_list = [
        '../output/demo2_1_table_0.jpg',
        '../output/demo2_1_table_1.jpg']
    test_query = "what's the rank of Alex's city?"
    test_pdf_content = get_pdf_content(pdf_path=pdf_file_path)
    make_request(pdf_content=test_pdf_content, images=table_images_list, query=test_query)
