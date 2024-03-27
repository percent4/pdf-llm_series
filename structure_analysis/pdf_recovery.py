# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: pdf_recovery.py
# @time: 2024/3/26 11:19
import os
import cv2
import json
import fitz
from PIL import Image
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="ch")


def paddle_ocr(image_path):
    result = ocr.ocr(image_path, cls=True)
    print(result)
    ocr_result = []
    for idx in range(len(result)):
        res = result[idx]
        if res:
            for line in res:
                ocr_result.append(line[1][0])
    return "".join(ocr_result)


def recover_pdf_page(page, page_height, page_image, page_res_txt_file):
    image = Image.open(page_image).convert('RGB')
    ratio = page_height/image.size[1]

    # data
    with open(page_res_txt_file, 'r') as f:
        content = [json.loads(_.strip()) for _ in f.readlines()]

    for i, line in enumerate(content):
        rect_type = line["type"]
        region = line["bbox"]
        region_img = image.crop((region[0] * 0.99, region[1] * 0.99, region[2] * 1.01, region[3] * 1.01))
        save_image_path = os.path.dirname(page_image) + f"/tmp_{i}.jpg"
        if rect_type in ["table", "figure"]:
            text_region = [int(_ * ratio) for _ in region]
            new_region_img = region_img.resize((text_region[2] - text_region[0], text_region[3] - text_region[1]))
            new_region_img.save(save_image_path)
            # 插入图片
            rect = fitz.Rect(text_region)
            page.insert_image(rect, filename=save_image_path)
        else:
            region_img.save(save_image_path)
            page.insert_font(
                fontname="HT",
                fontfile="/System/Library/Fonts/STHeiti Light.ttc")
            # 插入OCR识别后的文字
            region_text = paddle_ocr(image_path=save_image_path)
            text_region = [_ * ratio for _ in region]
            rect = fitz.Rect(text_region)
            shape = page.new_shape()
            line_height = 2 if "。" in region_text else 1
            shape.insert_textbox(rect, region_text, fontname='HT', fontsize=11, lineheight=line_height)
            shape.commit()


if __name__ == '__main__':
    doc = fitz.open()
    pdf_name = "book_split"
    pages = 3
    for i in range(pages):
        page = doc.new_page()
        page_height = page.bound().height
        pdf_image_path = f"../output/{pdf_name}/{pdf_name}_{i}.jpg"
        page_res_txt_file_path = f"../output/{pdf_name}/res_{i}.txt"
        recover_pdf_page(page=page, page_height=page_height, page_image=pdf_image_path, page_res_txt_file=page_res_txt_file_path)
    doc.ez_save(f"../data/{pdf_name}_recovery.pdf")
