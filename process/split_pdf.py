# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: split_pdf.py
# @time: 2024/3/1 16:23
import fitz


pdf_document = fitz.open("../data/book1.pdf")

# 构建输出文件名，以页数命名
output_pdf = f"../data/book_split.pdf"

# 创建一个新的Document对象，包含当前页面
new_pdf = fitz.open()
new_pdf.insert_pdf(pdf_document, from_page=0, to_page=2)

# 保存单独的PDF文件
new_pdf.save(output_pdf)
new_pdf.close()

pdf_document.close()
