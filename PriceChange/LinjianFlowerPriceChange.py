import chardet as chardet
import numpy as np
import openpyxl
import pandas as pd
import re
from datetime import datetime


now = datetime.now()
month = str(now.month).zfill(2)  # 月份补零
day = str(now.day).zfill(2)      # 日期补零
current_date = month + day


Store_Data_PATH = '../data/花店价格/价格初始表.xlsx'
Code_Name_PATH= '../data/花店价格/林间饿了么/林间商品0522.xlsx'

exclude_values = [
    '见面小花束',
    '草莓趴趴熊',
    '莓有烦恼',
    '甜酷蝴蝶',
    '小熊宇宙'
]

# 读取Excel文件
df = pd.read_excel(Store_Data_PATH,usecols=['商品名称','价格','店内一级分类'])
elm = pd.read_excel(Code_Name_PATH,usecols=['商品条形码','商品名称','店铺内一级分类名称'])
# 定义一个函数来提取【】内的花名
def extract_flower_name(name):
    match = re.search(r'【(.*?)】', str(name))
    if match:
        return match.group(1)
    return None

# 应用函数提取花名
df['花名'] = df['商品名称'].apply(extract_flower_name)
elm['花名'] = elm['商品名称'].apply(extract_flower_name)

# 过滤掉店内一级分类为“气球＆礼袋”的选项
df_filtered = df[~df['店内一级分类'].isin(['气球＆礼袋', '家居花区【温馨】'])]
elm_filtered = elm[~elm['店铺内一级分类名称'].isin(['气球＆礼袋', '家居花区【温馨】'])]

# 过滤掉多SKU链接
df_filtered = df_filtered[~df_filtered['花名'].isin(exclude_values)]
elm_filtered = elm_filtered[~elm_filtered['花名'].isin(exclude_values)]


# 输出花名和对应的价格
result = df_filtered[['花名', '价格']].dropna()

merged_df = pd.merge(elm_filtered,result,on='花名',how='left')
merged_df = merged_df.drop(['花名','商品名称','店铺内一级分类名称'],axis=1)


# 在两个列之间生成一个空白列，方便直接复制到饿了么模板表格里面去
col_position = 1
merged_df.insert(col_position,'自定义ID','')

merged_df.insert(col_position+2,'活动总库存','')
merged_df.insert(col_position+3,'每日活动库存','')
merged_df.insert(col_position+4,'每人/活动期间限购','')
merged_df.insert(col_position+5,'每人/每日限购','999')

#删除空行
merged_df = merged_df.dropna(subset=['价格'])

# 输出合并后的结果
output_path = "../data/花店价格/林间饿了么/林间饿了么代码导出价格.xlsx"

merged_df.to_excel(output_path,index=False)

print(merged_df)


