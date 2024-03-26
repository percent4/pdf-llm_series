# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: get_text_from_rectangle.py
# @time: 2024/3/20 15:33
import json

import fitz

doc = fitz.open('../data/llama_split.pdf')
page = doc[1]  # get first page
print(json.dumps(page.get_text("blocks", sort=True)))


def read_pdf_rect(origin_rect):
    # origin_rect = [316, 431, 404, 447]
    origin_rect = [_/2 for _ in origin_rect]
    rect = fitz.Rect(origin_rect)  # define your rectangle here
    text = page.get_textbox(rect)  # get text from rectangle
    string = text.replace('\n', '')
    return string


with open('../data/rect_0.txt', 'r') as f:
    lines = [json.loads(_.strip()) for _ in f.readlines()]

rect_text_dict = {}
for line in lines:
    rect = line["bbox"]
    rect_text_dict[",".join([str(_) for _ in rect])] = read_pdf_rect(origin_rect=rect)

doc.close()

print(rect_text_dict)

