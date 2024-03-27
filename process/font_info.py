# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: font_info.py
# @time: 2024/3/26 17:52
import fitz

font = fitz.Font(
    fontname="HT",
    fontfile="/System/Library/Fonts/STHeiti Light.ttc")

doc = fitz.open()
page = doc.new_page()
w_text = "你好"
w_rect = (20, 20, 100, 100)


def calc_distance(point1, point2):
    return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2


def get_most_suitable_font_size(page, write_rect, write_text):
    min_dist = 100000
    suitable_font_size = 5
    tw = fitz.TextWriter(page.rect)
    for font_size in range(10, 50, 1):
        font_size_used = font_size / 2
        tw.fill_textbox(
            rect=(write_rect[0], write_rect[1], write_rect[2], page.rect[3]),
            text=write_text,
            pos=(write_rect[0], write_rect[1]),
            font=font,
            fontsize=font_size_used,
            lineheight=1.2)
        last_point_x, last_point_y = tw.last_point.x, tw.last_point.y
        dist = calc_distance([last_point_x, last_point_y], [write_rect[2], write_rect[3]])
        if last_point_x < write_rect[2] and last_point_y < write_rect[3] and dist < min_dist:
            suitable_font_size = font_size_used
            min_dist = dist
    return suitable_font_size


s_font_size = get_most_suitable_font_size(page=page, write_rect=w_rect, write_text=w_text)
print("s_font_size", s_font_size)
tw = fitz.TextWriter(page.rect)
tw.fill_textbox(rect=w_rect, text=w_text, pos=(w_rect[0], w_rect[1]), font=font, fontsize=s_font_size, lineheight=1.2)
tw.write_text(page=page)
doc.ez_save("x.pdf")
