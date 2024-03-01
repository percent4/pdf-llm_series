# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: get_text_from_scanned_pdf.py
# @time: 2024/3/1 15:24
import fitz
from PIL import Image
import os
import cv2
import json
import base64
import requests
from openai import OpenAI


def convert_pdf_2_img(pdf_file: str, pages: int) -> None:
    pdf_document = fitz.open(pdf_file)

    # Iterate through each page and convert to an image
    for page_number in range(pages):
        # Get the page
        page = pdf_document[page_number]
        # Convert the page to an image
        pix = page.get_pixmap()
        # Create a Pillow Image object from the pixmap
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        # Save the image
        image.save(f"../output/book1_{page_number + 1}.png")

    # Close the PDF file
    pdf_document.close()


def cv2_to_base64(img):
    data = cv2.imencode('.jpg', img)[1]
    return base64.b64encode(data.tobytes()).decode('utf8')


def image_ocr(image_path):
    # get ocr result
    data = {'images': [cv2_to_base64(cv2.imread(image_path))]}
    headers = {"Content-type": "application/json"}
    url = "http://localhost:50076/predict/ch_pp-ocrv3"
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    if r.json()["results"]:
        return "\n".join([ocr_record["text"].strip() for ocr_record in r.json()["results"][0]["data"]])
    else:
        return ""


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
    test_pdf_file = "../data/book1.pdf"
    convert_pdf_2_img(pdf_file=test_pdf_file, pages=2)
    page1_ocr_result = image_ocr("../output/book1_2.png")
    print(f"识别文字内容: {page1_ocr_result}")

    query1 = "破浪理论的创始人是谁，他的出生年月？"
    predict_answer = get_answer(pdf_content=page1_ocr_result, query=query1)
    print("回答:", predict_answer)


"""
识别文字内容: 作者简介
R.N.艾略特（1871-1948），波浪理论的创始人，
曾当过会计师，就职于铁路公司、餐饮等多种行业。
人们对他的身世了解不多，1934年出版《波浪原理》，
为这一重要理论奠定了坚实的基础。他的理论由于
艰深难懂而被人们长期忽视。1978年，他的思想的
直接继承者帕御特出版了与人合著的《波浪理论》一
书，并在期权交易竞赛中取得四个月获得400%以上
的轿人成绩，从而使波浪原理迅速传播。现在的任
何一部股市理论教科书中波浪理论都占有越来越大
的篇幅。
ee more oleasevisit:htuos/nomeoto
回答: 破浪理论的创始人是R.N.艾略特，他出生于1871年。
"""
