# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: get_table_images.py
# @time: 2024/3/28 14:08
import os
import re
import json

from PIL import Image


class TableConvert(object):
    def __init__(self, res_dir):
        self.res_dir = res_dir

    @staticmethod
    # 解析每页PDF中的表格，保存为图片
    def parse_table(pdf_page_image, pdf_res_txt):
        dir_name = os.path.dirname(pdf_page_image)
        page_number = re.findall("\\d+", pdf_page_image)[-1]
        with open(pdf_res_txt, 'r') as f:
            content = [json.loads(_.strip()) for _ in f.readlines()]

        table_cnt = 1
        for line in content:
            rect_type = line["type"]
            region = line["bbox"]
            # 插入表格、图片
            if rect_type == "table":
                with Image.open(pdf_page_image).convert('RGB') as image:
                    region_img = image.crop(region)
                    save_image_path = f"{dir_name}/table_{page_number}_{table_cnt}.jpg"
                    print(f"save table to {save_image_path}")
                    region_img.save(save_image_path, 'JPEG', quality=95)
                    table_cnt += 1

    # 解析版面分析后的PDF结果的文件夹
    def get_tables_into_image(self):
        pdf_name = self.res_dir.split("/")[-1]
        for file in os.listdir(self.res_dir):
            if file.startswith(pdf_name):
                res_txt = file.replace(pdf_name, "res").replace("jpg", "txt")
                pdf_page_image_path = os.path.join(self.res_dir, file)
                pdf_res_txt_path = os.path.join(self.res_dir, res_txt)
                self.parse_table(
                    pdf_page_image=pdf_page_image_path,
                    pdf_res_txt=pdf_res_txt_path)


if __name__ == '__main__':
    output_dir = '../output/BLOOM'
    table_convertor = TableConvert(res_dir=output_dir)
    table_convertor.get_tables_into_image()
