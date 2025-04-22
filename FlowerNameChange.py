import chardet as chardet
import numpy as np
import openpyxl
import os
import pandas as pd
import re



Store_Data_PATH = 'data/花店价格/美团商品0310.xlsx'
Code_Name_PATH= 'data/花店价格/林间0317.xlsx'
Flower_Name_PATH = 'data/花店上架图片'

exclude_values = [
    '见面小花束',
    '草莓趴趴熊',
    '莓有烦恼',
    '春日来信'
]

# 读取Excel文件
elm = pd.read_excel(Code_Name_PATH,usecols=['商品条形码','商品名称','店铺内一级分类名称'])
# 定义一个函数来提取【】内的花名
def extract_flower_name(name):
    match = re.search(r'【(.*?)】', str(name))
    if match:
        return match.group(1)
    return None

# 应用函数提取花名
elm['花名'] = elm['商品名称'].apply(extract_flower_name)

# 过滤掉店内一级分类为“气球＆礼袋”的选项
elm_filtered = elm[~elm['店铺内一级分类名称'].isin(['气球＆礼袋', '家居花区【温馨】'])]

# 过滤掉多SKU链接
elm_filtered = elm_filtered[~elm_filtered['花名'].isin(exclude_values)]


elm_filtered = elm_filtered.drop(['商品名称','店铺内一级分类名称'],axis=1)


print(elm_filtered)


def rename_images_by_barcode(df, image_folder, log_file='error.log'):
    """
    :param mapping_file: 映射文件路径（支持CSV/Excel，需包含'条形码'和'花名'两列）
    :param image_folder: 图片文件夹路径
    :param log_file: 错误日志文件名
    """
    # 读取映射文件

    name_to_barcode = dict(zip(df['花名'], df['商品条形码']))

    # 初始化错误日志
    with open(log_file, 'w') as f:
        f.write("未成功重命名的文件：\n")

    # 遍历图片文件
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # 提取花名和扩展名
            flower_name, ext = os.path.splitext(filename)

            # 匹配条形码
            if flower_name in name_to_barcode:
                new_name = f"{name_to_barcode[flower_name]}{ext}"
                old_path = os.path.join(image_folder, filename)
                new_path = os.path.join(image_folder, new_name)

                # 避免覆盖已存在文件
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f"成功：{filename} -> {new_name}")
                else:
                    with open(log_file, 'a') as f:
                        f.write(f"{filename} | 目标文件已存在\n")
            else:
                with open(log_file, 'a') as f:
                    f.write(f"{filename} | 未找到对应条形码\n")


if __name__ == '__main__':
    rename_images_by_barcode(
        df = elm_filtered,
        image_folder= Flower_Name_PATH  # 替换为图片文件夹路径
    )

