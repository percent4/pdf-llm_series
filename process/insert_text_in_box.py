# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: insert_text_in_box.py
# @time: 2024/3/21 17:00
import fitz

red = fitz.pdfcolor["red"]  # some colors
blue = fitz.pdfcolor["blue"]

doc = fitz.open()  # new or existing PDF
page = doc.new_page()  # new page, or choose doc[n]
page.insert_font(fontname="HT", fontfile="/System/Library/Fonts/STHeiti Light.ttc")
# write in this overall area
rect = fitz.Rect(609/2, 1016/2, 1051/2, 1545/2)
t1 = '与 Chinchilla、PaLM 或 GPT-3 不同的是，我们只使用公开可用的数据，这使得我们的工作与开源兼容，而大多数现有模型依赖的数据要么不公开可用，要么没有记录（例如 "书籍 - 2TB" 或 "社交媒体对话"）。但也有一些例外，尤其是 OPT（Zhang 等人，2022 年）、GPT-NeoX（Black 等人，2022 年）、BLOOM（Scaoet 等人，2022 年）和 GLM（Zeng 等人，2022 年），但它们都无法与 PaLM-62B 或 Chinchilla 竞争。在本文的其余部分，我们将概述我们对转换器架构（Vaswani 等人，2017 年）所做的修改，以及我们的训练方法。然后，我们报告了我们模型的性能，并在一组标准基准上与其他 LLM 进行了比较。最后，我们利用负责任的人工智能社区的一些最新基准，揭示了我们的模型中编码的一些偏差和毒性。'
shape = page.new_shape()  # create Shape
shape.insert_textbox(rect, t1, fontname='HT', fontsize=12)
shape.draw_rect(rect)
shape.finish(width=0.3, color=red)
shape.commit()  # write all stuff to the page
doc.ez_save("../output/insert_textbox_demo.pdf")
