import chardet as chardet
import numpy as np
import openpyxl
import pandas as pd
import re



Store_Data_PATH = 'data/花店价格/美团降价0418.xlsx'
Code_Name_PATH= 'data/花店价格/抖音小时达/抖音价格0417.xlsx'

exclude_values = [
    '见面小花束',
    '草莓趴趴熊',
    '莓有烦恼',
    '春日来信',
    '午后红茶',
    '甜酷蝴蝶'
]

# 读取Excel文件
df = pd.read_excel(Store_Data_PATH,usecols=['商品名称','价格','店内一级分类'])
dy = pd.read_excel(Code_Name_PATH,sheet_name='参考信息-商品+规格ID',usecols=['商品ID','商品名称']).to_csv('data/花店价格/抖音小时达/抖音价格.csv',index=False)
dy = pd.read_csv('data/花店价格/抖音小时达/抖音价格.csv',encoding='utf-8')

# 定义一个函数来提取【】内的花名
def extract_flower_name(name):
    match = re.search(r'【(.*?)】', str(name))
    if match:
        return match.group(1)
    return None

# 应用函数提取花名
df['花名'] = df['商品名称'].apply(extract_flower_name)
dy['花名'] = dy['商品名称'].apply(extract_flower_name)

# 过滤掉店内一级分类为“气球＆礼袋”的选项
df_filtered = df[~df['店内一级分类'].isin(['气球＆礼袋', '家居花区【温馨】'])]

# 过滤掉多SKU链接
df_filtered = df_filtered[~df_filtered['花名'].isin(exclude_values)]
dy_filtered = dy[~dy['花名'].isin(exclude_values)]


# 输出花名和对应的价格
result = df_filtered[['花名', '价格']].dropna()

merged_df = pd.merge(dy,result,on='花名',how='left')
merged_df = merged_df.drop(['花名','商品名称'],axis=1)

# 在两个列之间生成一个空白列，方便直接复制到抖音模板表格里面去
col_position = merged_df.columns.get_loc('商品ID') + 1

merged_df.insert(col_position,'规格ID','all')

#删除空行
merged_df = merged_df.dropna(subset=['价格'])


# 输出合并后的结果
output_path = "data/花店价格/抖音小时达/抖音复制价格.xlsx"

merged_df['商品ID'] = merged_df['商品ID'].astype(str)

merged_df.to_excel(output_path,index=False)

print(merged_df)


