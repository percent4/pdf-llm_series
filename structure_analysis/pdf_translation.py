# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: pdf_translation.py
# @time: 2024/3/26 22:03
import os
import json
import fitz
from PIL import Image
from llm.deepl_translation import translate_api

FONT_NAME = 'HT'
FONT_FILE = '/System/Library/Fonts/STHeiti Light.ttc'
font = fitz.Font(
    fontname="HT",
    fontfile="/System/Library/Fonts/STHeiti Light.ttc")


def calc_distance(point1, point2):
    return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2


def get_most_suitable_font_size(page, write_rect, write_text, line_height):
    min_dist = 10000
    suitable_font_size = 5.0
    tw = fitz.TextWriter(page.rect)
    for font_size in range(10, 41, 1):
        font_size_used = font_size / 2
        tw.fill_textbox(
            rect=(write_rect[0], write_rect[1], write_rect[2], page.rect[3]),
            text=write_text,
            pos=(write_rect[0], write_rect[1]),
            font=font,
            fontsize=font_size_used,
            lineheight=line_height)
        last_point_x, last_point_y = tw.last_point.x, tw.last_point.y
        dist = calc_distance([last_point_x, last_point_y], [
                             write_rect[2], write_rect[3]])
        if last_point_x < write_rect[2] and last_point_y < write_rect[3] and dist < min_dist:
            suitable_font_size = font_size_used
            min_dist = dist
    return suitable_font_size


def recover_pdf_page(
        read_page,
        write_page,
        page_height,
        page_image,
        page_res_txt_file):
    image = Image.open(page_image).convert('RGB')
    ratio = page_height / image.size[1]

    # read res data
    with open(page_res_txt_file, 'r') as f:
        content = [json.loads(_.strip()) for _ in f.readlines()]

    for line in content:
        rect_type = line["type"]
        region = line["bbox"]
        # 插入表格、图片
        if rect_type in ["table", "figure"]:
            region_img = image.crop(region)
            save_image_path = os.path.dirname(page_image) + "/tmp.jpg"
            img_region = [int(_ * ratio) for _ in region]
            new_region_img = region_img.resize(
                (img_region[2] - img_region[0], img_region[3] - img_region[1]))
            new_region_img.save(save_image_path, 'JPEG', quality=95)
            write_page.insert_image(img_region, filename=save_image_path)
        else:
            # 读取文字
            text_region = [int(_ * ratio) for _ in region]
            rect = fitz.Rect(text_region)
            text = read_page.get_textbox(rect)
            string = text.replace('\n', '')
            write_page.insert_font(fontname=FONT_NAME, fontfile=FONT_FILE)
            # 插入翻译后的文字
            translate_string = translate_api(text=string)
            # shape = write_page.new_shape()
            line_height = 1.5 if "。" in translate_string else 1
            font_size_to_use = get_most_suitable_font_size(
                page=write_page,
                write_text=translate_string,
                write_rect=text_region,
                line_height=line_height)
            print(
                f"\ntext: {string}\ntranslate text: {translate_string}\nfont size: {font_size_to_use}\n")
            tw = fitz.TextWriter(write_page.rect)
            tw.fill_textbox(
                rect=text_region,
                text=translate_string,
                pos=(
                    text_region[0],
                    text_region[1]),
                font=font,
                fontsize=font_size_to_use,
                lineheight=line_height)
            tw.write_text(page=write_page)


if __name__ == '__main__':
    read_doc = fitz.open('../data/llama_split.pdf')
    write_doc = fitz.open()
    pdf_name = "llama_split"
    pages = 6
    for i in range(pages):
        read_page = read_doc[i]
        write_page = write_doc.new_page()
        page_height = write_page.bound().height
        pdf_image_path = f"../output/{pdf_name}/{pdf_name}_{i}.jpg"
        page_res_txt_file_path = f"../output/{pdf_name}/res_{i}.txt"
        recover_pdf_page(
            read_page=read_page,
            write_page=write_page,
            page_height=page_height,
            page_image=pdf_image_path,
            page_res_txt_file=page_res_txt_file_path)
    write_doc.ez_save(f"../data/{pdf_name}_translate.pdf")
    write_doc.close()
    read_doc.close()
