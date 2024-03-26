# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: insert_text_in_box.py
# @time: 2024/3/21 17:00
import fitz
from llm.deepl_translation import translate_api

doc = fitz.open('../data/llama_split.pdf')
page = doc[1]  # get first page
page_blocks = page.get_text("blocks", sort=True)
doc.close()

red = fitz.pdfcolor["red"]  # some colors
blue = fitz.pdfcolor["blue"]

doc = fitz.open()  # new or existing PDF
page = doc.new_page()  # new page, or choose doc[n]
page.insert_font(
    fontname="HT",
    fontfile="/System/Library/Fonts/STHeiti Light.ttc")


def write_pdf(rect, origin_text, translated_text):
    # write in this overall area
    fontsize_to_use = (rect[3] - rect[1]) * 0.8 / origin_text.count('\n')
    print(f"font size: {fontsize_to_use}")
    rect = fitz.Rect(rect)
    shape = page.new_shape()  # create Shape
    shape.insert_textbox(rect, translated_text, fontname='HT', fontsize=fontsize_to_use)
    # shape.draw_rect(rect)
    # shape.finish(width=0.3, color=red)
    shape.commit()  # write all stuff to the page


for block in page_blocks:
    pdf_rect = block[:4]
    print('-->', pdf_rect)
    pdf_text = block[4]
    translate_text = translate_api(text=pdf_text.replace('\n', ' '))
    print("text: {}, translated_text: {}".format(pdf_text.replace('\n', ' '), translate_text))
    write_pdf(rect=pdf_rect, origin_text=pdf_text, translated_text=translate_text)

doc.ez_save("../output/insert_textbox_demo.pdf")
