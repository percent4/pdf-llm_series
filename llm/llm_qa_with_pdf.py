# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: llm_qa_with_pdf.py
# @time: 2024/3/1 13:46
import os
import fitz
from openai import OpenAI


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


def get_answer(pdf_content: str, query: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"The full text of PDF file is: {pdf_content}"},
            {"role": "user", "content": query}
        ],
        max_tokens=1000
    )

    answer = response.choices[0].message.content

    return answer


if __name__ == '__main__':
    content = get_pdf_content("../data/oppo_n3_flip.pdf")
    query1 = "OPPO Find N3 Flip的价格？"
    print(get_answer(pdf_content=content, query=query1))

    query2 = "蚂蚁集团发布的大模型叫什么？"
    print(get_answer(pdf_content=content, query=query2))

    query3 = "混元大模型是什么时候发布的？"
    print(get_answer(pdf_content=content, query=query3))

"""
OPPO Find N3 Flip有两个版本可选，分别是12GB+256GB和12GB+512GB。起售价为6799元人民币。
蚂蚁集团发布的大模型叫做"大图模型"（Large Graph Model，简称LGM）。
混元大模型是在2023年9月7日，在2023腾讯全球数字生态大会上正式对外亮相的。
"""
