# -*- coding: utf-8 -*-
# @place: Pudong, Shanghai
# @file: get_table_and_caption.py
# @time: 2024/3/28 10:38
# use fitz to get table and its caption from pdf file
import math
import os
import json
import re
from operator import itemgetter
import fitz
from PIL import Image
# 为图片或表格匹配对应的caption


class TableFigureMatch(object):
    def __init__(self, pdf_file_path, res_dir):
        self.pdf_file_path = pdf_file_path
        self.res_dir = res_dir

    # get table or figure caption in each PDF page
    def get_caption_by_page(self, data_type):
        """
        :param data_type: str, data type from pdf, enumerate: table or figure
        :return: page_dict_list: list[dict], data type dict in each page in list
        """
        assert data_type in ['table', 'figure']
        doc = fitz.open(self.pdf_file_path)
        page_number = doc.page_count
        page_dict_list = []
        for i in range(page_number):
            table_page_dict = {}
            page = doc[i]
            page_dict = page.get_text("dict", sort=True)
            for block in page_dict['blocks']:
                bbox = block['bbox']
                text_list = []
                if 'lines' in block:
                    for spans in block['lines']:
                        for span in spans['spans']:
                            text_list.append(span['text'])
                    text = ' '.join(text_list)
                    if text.lower().startswith(data_type):
                        table_page_dict['-'.join([str(x) for x in bbox])] = text
            page_dict_list.append(table_page_dict)
        page_height = page_dict['height']
        doc.close()
        return page_height, page_dict_list

    def get_pdf_img_ration(self, pdf_height):
        path_name = self.pdf_file_path.split('/')[-1].split('.')[0]
        image_path = os.path.join(self.res_dir, f"{path_name}_0.jpg")
        with Image.open(image_path).convert('RGB') as image:
            image_height = image.height
        return pdf_height/image_height

    @staticmethod
    def find_rect_center(rect):
        return (rect[0]+rect[2])/2, (rect[1]+rect[3])/2

    @staticmethod
    def get_euclid_distance(x0, y0, x1, y1):
        return math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    def find_neighbor_rect(self, rect1, rect_list):
        if len(rect_list) == 1:
            return rect_list[0]
        center_x_rect1, center_y_rect1 = self.find_rect_center(rect1)
        center_rect_list = []
        for rect in rect_list:
            center_x, center_y = self.find_rect_center(rect)
            center_rect_list.append((center_x, center_y))

        distance_dict = {}
        for i, center in enumerate(center_rect_list):
            distance = self.get_euclid_distance(center_x_rect1, center_y_rect1, center[0], center[1])
            distance_dict[i] = distance
        distance_sort_list = sorted(distance_dict.items(), key=itemgetter(1))
        return rect_list[distance_sort_list[0][0]]

    def match_caption_by_page(self, data_type):
        data_type_caption_dict = {}
        pdf_height, page_dict_list = self.get_caption_by_page(data_type=data_type)
        pdf_img_ration = self.get_pdf_img_ration(pdf_height=pdf_height)
        for file in os.listdir(self.res_dir):
            if file.startswith("res"):
                pg_num = int(re.findall('\d+', file)[0])
                res_txt_file_path = os.path.join(self.res_dir, file)
                with open(res_txt_file_path, 'r') as f:
                    content = [json.loads(_.strip()) for _ in f.readlines()]
                cnt = 1
                for line in content:
                    rect_type, rect_bbox = line['type'], line['bbox']
                    pdf_rect_bbox = [_ * pdf_img_ration for _ in rect_bbox]
                    if rect_type == data_type and page_dict_list[pg_num]:
                        caption_rect_list = [[float(x) for x in _.split('-')]for _ in page_dict_list[pg_num].keys()]
                        neighbor_rect = self.find_neighbor_rect(rect1=pdf_rect_bbox, rect_list=caption_rect_list)
                        if data_type == 'table':
                            file_path = f'table_{pg_num}_{cnt}.jpg'
                            cnt += 1
                        else:
                            file_path = f"[{', '.join([str(_) for _ in rect_bbox])}]_{pg_num}.jpg"
                        data_type_caption_dict[file_path] = page_dict_list[pg_num]['-'.join([str(_) for _ in neighbor_rect])]
        return data_type_caption_dict

    def run(self):
        data_type_dict = {}
        for data_type in ['table', 'figure']:
            data_type_caption_dict = self.match_caption_by_page(data_type=data_type)
            data_type_dict.update(data_type_caption_dict)

        with open(os.path.join(self.res_dir, "table_figure_caption.json"), "w") as f:
            f.write(json.dumps(data_type_dict, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    pdf_path = '../data/BLOOM.pdf'
    res_output_dir = '../output/BLOOM'
    table_figure_matcher = TableFigureMatch(pdf_file_path=pdf_path, res_dir=res_output_dir)
    table_figure_matcher.run()
