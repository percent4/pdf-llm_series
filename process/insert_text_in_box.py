# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: insert_text_in_box.py
# @time: 2024/3/21 17:00
import fitz
from llm.deepl_translation import translate_api

doc = fitz.open('../data/llama_split.pdf')
page = doc[1]  # get first page
page_dict = page.get_text("dict", sort=True)
page_blocks = page.get_text("blocks", sort=True)
doc.close()


def rect_contains(rect_big, rect_small):
    if rect_small[0] >= rect_big[0] and rect_small[1] >= rect_big[1] and rect_small[2] <= rect_big[2] and rect_small[3] <= rect_big[3]:
        return True
    return False


def find_block_font_info(block_text, block_bbox):
    for block in page_dict["blocks"]:
        bbox = block["bbox"]
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"]
                text_block_bbox = span["bbox"]
                if text in block_text and rect_contains(
                        rect_big=block_bbox, rect_small=text_block_bbox):
                    return span["size"], span["ascender"] - span["descender"]


doc = fitz.open()  # new or existing PDF
page = doc.new_page()  # new page, or choose doc[n]
page.insert_font(
    fontname="HT",
    fontfile="/System/Library/Fonts/STHeiti Light.ttc")


def write_pdf(rect, origin_text, translated_text):
    # write in this overall area
    font_size, line_height = find_block_font_info(
        block_text=origin_text, block_bbox=rect)
    print(rect, f"font size: {font_size}, line height: {line_height}")
    rect = fitz.Rect(rect)
    shape = page.new_shape()  # create Shape
    shape.insert_textbox(
        rect,
        translated_text,
        fontname='HT',
        fontsize=font_size * 0.85,
        lineheight=line_height)
    # shape.draw_rect(rect)
    # shape.finish(width=0.3, color=red)
    shape.commit()  # write all stuff to the page


for block in page_blocks:
    pdf_rect = block[:4]
    print('-->', pdf_rect)
    pdf_text = block[4]
    translate_text = translate_api(text=pdf_text.replace('\n', ' '))
    print("text: {}, translated_text: {}".format(
        pdf_text.replace('\n', ' '), translate_text))
    write_pdf(
        rect=pdf_rect,
        origin_text=pdf_text,
        translated_text=translate_text)

doc.ez_save("../output/insert_textbox_demo_1.pdf")
