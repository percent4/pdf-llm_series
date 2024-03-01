# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: get_images_from_pdf.py
# @time: 2024/3/1 10:59
# PyMuPDF==1.23.26
import fitz

pdf_path = "../data/demo1.pdf"
doc = fitz.open(pdf_path)

# basic PDF info
title = doc.metadata["title"]
author = doc.metadata["author"]
create_date = doc.metadata["creationDate"]
num_pages = doc.page_count
page = doc.load_page(0)
page_height = page.bound().height
page_width = page.bound().width
print(f"title: {title}\nauthor: {author}\ncreate_date: {create_date}\nnum_pages: {num_pages}\n"
      f"page_height: {page_height}\npage_width: {page_width}\n")

# Text info of PDF
for page_index in range(num_pages):
    page = doc.load_page(page_index)
    text = page.get_text()
    print(f"第{page_index + 1}页的文本内容为：\n{text}\n")

# Image info of PDF
for page_index in range(num_pages):
    page = doc.load_page(page_index)
    image_list = page.get_images()
    print(image_list)
    for img in image_list:
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        print(pix.colorspace, '-->', fitz.csRGB)
        img_path = f'../output/image{page_index + 1}_{xref}.png'
        pix.save(img_path)

# 关闭文件
doc.close()
