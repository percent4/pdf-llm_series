# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: merge_pdf.py
# @time: 2024/3/7 20:05
import fitz

# The list of filenames.
filelist = ["../data/demo1.pdf", "../data/demo2.pdf"]

# The desired output document. In this case, we choose a new PDF.
doc = fitz.open()

# Now loop through names of input files to insert each.
for filename in filelist:
    doc.insert_file(filename)

# save it to disk, giving it a desired file name.
doc.save("../output/demo.pdf")
doc.close()
