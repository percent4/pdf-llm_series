# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: get_text_from_rectangle.py
# @time: 2024/3/20 15:33
import fitz

doc = fitz.open('../data/llama_split.pdf')
page = doc[0]  # get first page
# print(page.get_text("dict", sort=True))
rect = fitz.Rect(609/2, 1016/2, 1051/2, 1545/2)  # define your rectangle here
text = page.get_textbox(rect)  # get text from rectangle
print(text.replace('\n', ''))
doc.close()

"""
Unlike Chinchilla, PaLM, or GPT-3, we onlyuse publicly available data, making our work com-patible with open-sourcing, while most existingmodels rely on data which is either not publiclyavailable or undocumented (e.g. “Books – 2TB” or“Social media conversations”). There exist someexceptions, notably OPT (Zhang et al., 2022),GPT-NeoX (Black et al., 2022), BLOOM (Scaoet al., 2022) and GLM (Zeng et al., 2022), but nonethat are competitive with PaLM-62B or Chinchilla.In the rest of this paper, we present an overviewof the modifications we made to the transformerarchitecture (Vaswani et al., 2017), as well as ourtraining method. We then report the performance ofour models and compare with others LLMs on a setof standard benchmarks. Finally, we expose someof the biases and toxicity encoded in our models,using some of the most recent benchmarks fromthe responsible AI community.
"""