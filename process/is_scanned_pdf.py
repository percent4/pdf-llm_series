# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: is_scanned_pdf.py
# @time: 2024/3/8 10:06
import fitz
import time

s_time = time.time()
pdf_path = "../data/oppo_n3_flip.pdf"
doc = fitz.open(pdf_path)
num_pages = doc.page_count

text_list = []
for page_index in range(num_pages):
    page = doc.load_page(page_index)
    text = page.get_text()
    text_list.append(text)

print(''.join(text_list))
print('different pages: ', len(set(text_list)))     # when pages > 1, it may be useful
print(f'cost time: {time.time() - s_time}')
