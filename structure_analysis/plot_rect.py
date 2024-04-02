import cv2 
import json
   
# path  
path = '../output/BLOOM/BLOOM_29.jpg'
image = cv2.imread(path)
print(image.shape)
   
# data
res_path = '../output/BLOOM/res_29.txt'
with open(res_path, 'r') as f:
    content = [json.loads(_.strip()) for _ in f.readlines()]

for line in content:
    start_point = (line["bbox"][0], line["bbox"][1])
    end_point = (line["bbox"][2], line["bbox"][3])
    if line["type"] == "text":  # 文字
        color = (0, 0, 255)
    elif line["type"] == "table":   # 表格
        color = (0, 255, 0)
    else:   # 图片
        color = (255, 0, 0)
    image = cv2.rectangle(image, start_point, end_point, color, 1) 
  
# Displaying the image
save_path = path.split(".jpg")[0] + "_rect.jpg"
cv2.imwrite(save_path, image)
