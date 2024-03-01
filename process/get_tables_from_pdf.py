# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: get_tables_from_pdf.py
# @time: 2024/3/1 14:39
import fitz

doc = fitz.open('../data/demo2.pdf')
page = doc[0]   # 提取第1页中的所有表格
tables = page.find_tables()
print(f"tables: {tables}")
for i, table in enumerate(tables):
    df = tables[0].to_pandas()
    df.to_csv(f'../output/table_pg_{1}_{i + 1}.csv', index=False)
