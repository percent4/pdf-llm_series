# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: get_text_from_rectangle.py
# @time: 2024/3/20 15:33
import fitz

doc = fitz.open('../data/llama_split.pdf')
page = doc[0]  # get first page
rect = fitz.Rect(609/2, 1016/2, 1051/2, 1545/2)  # define your rectangle here
text = page.get_textbox(rect)  # get text from rectangle
print(text)
doc.close()
