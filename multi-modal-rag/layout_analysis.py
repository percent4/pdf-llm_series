# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: layout_analysis.py
# @time: 2024/4/3 10:52
# use PP-Structure V2 to get layout analysis for PDF
import os
import re
import json
import cv2
import fitz
from PIL import Image
from paddleocr import PPStructure, save_structure_res


class LayoutAnalysis(object):
    def __init__(self, pdf_file_path, save_folder="../output"):
        self.pdf_file_path = pdf_file_path
        self.save_folder = save_folder
        self.file_name = os.path.basename(self.pdf_file_path).split('.')[0]
        self.save_dir = os.path.join(self.save_folder, f"{self.file_name}")
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def _convert_to_img(self):
        pdf_document = fitz.open(self.pdf_file_path)
        image_path_list = []
        # Iterate through each page and convert to an image
        for page_number in range(pdf_document.page_count):
            # Get the page
            page = pdf_document[page_number]
            # Convert the page to an image
            pix = page.get_pixmap()
            # Create a Pillow Image object from the pixmap
            image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            # Save the image
            image_path = os.path.join(self.save_dir, f"{self.file_name}_{page_number + 1}.jpg")
            image_path_list.append(image_path)
            image.save(image_path, "JPEG", quality=95)
        # Close the PDF file
        pdf_document.close()
        return image_path_list

    def image_parse(self):
        image_path_list = self._convert_to_img()
        table_engine = PPStructure(table=False, ocr=False, show_log=True)
        for img_idx, img_path in enumerate(image_path_list):
            print(f"Layout analysis for {img_idx+1} image with path: {img_path}")
            img = cv2.imread(img_path)
            result = table_engine(img)
            save_structure_res(result, self.save_folder, self.file_name, img_idx=img_idx+1)
            for line in result:
                line.pop('img')
                print(line)

    @staticmethod
    # 解析每页PDF中的表格，保存为图片
    def parse_table(pdf_page_image, pdf_res_txt):
        dir_name = os.path.dirname(pdf_page_image)
        page_number = re.findall("\d+", pdf_page_image)[-1]
        with open(pdf_res_txt, 'r') as f:
            content = [json.loads(_.strip()) for _ in f.readlines()]

        table_cnt = 1
        for line in content:
            rect_type = line["type"]
            region = line["bbox"]
            # 将表格保存为图片
            if rect_type == "table":
                with Image.open(pdf_page_image).convert('RGB') as image:
                    region_img = image.crop(region)
                    save_image_path = f"{dir_name}/{page_number}_{table_cnt}_table.jpg"
                    print(f"save table to {save_image_path}")
                    region_img.save(save_image_path, 'JPEG', quality=95)
                    table_cnt += 1

    # 解析版面分析后的PDF结果的文件夹
    def tables_2_images(self):
        for file in os.listdir(self.save_dir):
            if file.startswith(self.file_name):
                res_txt = file.replace(self.file_name, "res").replace("jpg", "txt")
                pdf_page_image_path = os.path.join(self.save_dir, file)
                pdf_res_txt_path = os.path.join(self.save_dir, res_txt)
                self.parse_table(pdf_page_image=pdf_page_image_path,
                                 pdf_res_txt=pdf_res_txt_path)

    def run(self):
        self.image_parse()
        self.tables_2_images()


if __name__ == '__main__':
    pdf_path = "../data/Attention.pdf"
    layout_analyzer = LayoutAnalysis(pdf_file_path=pdf_path)
    layout_analyzer.run()
