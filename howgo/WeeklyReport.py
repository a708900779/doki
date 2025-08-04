import pandas as pd
import numpy as np
from datetime import datetime

now = datetime.now()
month = str(now.month).zfill(2)  # 月份补零
day = str(now.day).zfill(2)      # 日期补零
current_date = month + day



DATA_PATH = "../data/howgo数据/天猫数据"+current_date+".xls"
MAPPING_PATH = "../data/howgo数据/天猫商品ID和名称对应表.xlsx"

# 读取主数据表（兼容.xls格式）
df_main = pd.read_excel(DATA_PATH, engine='xlrd',skiprows=4)

# 读取商品ID与简称对应表
df_mapping = pd.read_excel(MAPPING_PATH,skiprows=4)

# 提取指定列并按顺序定义
required_columns = [
    '统计日期', '商品ID', '商品访客数', '搜索引导访客数',
    '搜索引导支付买家数', '搜索引导支付转化率', '支付金额',
    '成功退款金额', '支付买家数','商品支付转化率', '商品收藏人数',
    '商品加购件数',  '访客平均价值'
]
df_main = df_main[required_columns]

# 计算真实销售额（支付金额 - 成功退款金额）

# 方法1：使用 astype() 强制转换（需确保无非法字符）
# 示例：去除货币符号和千分位分隔符
df_main["支付金额"] = df_main["支付金额"].astype(str).str.replace(r"[¥,]", "", regex=True).astype(float)
df_main["成功退款金额"] = df_main["成功退款金额"].astype(str).str.replace(r"[¥,]", "", regex=True).astype(float)


df_main["支付金额"] = df_main["支付金额"].astype(float)
df_main["成功退款金额"] = df_main["成功退款金额"].astype(float)



real_sales = df_main['支付金额'] - df_main['成功退款金额']
aov = (real_sales / df_main['支付买家数']).round(1)

# 插入新列到指定位置（商品简称和商品访客数之间）
# 步骤说明：
# 1. 获取当前列的索引位置
current_cols = df_main.columns.tolist()
insert_pos = current_cols.index('商品访客数')  # 在商品访客数之前插入

# 2. 从后往前插入以保证顺序正确
df_main.insert(insert_pos, '客单价', aov)     # 插入空列[3,6](@ref)
df_main.insert(insert_pos, '老客销售额占比', np.nan)     # 插入空列[3,6](@ref)
df_main.insert(insert_pos, '老客销售额', np.nan)     # 插入空列[3,6](@ref)
df_main.insert(insert_pos, '推广占比', np.nan)  # 插入空列[3,6](@ref)
df_main.insert(insert_pos, '推广费', np.nan)     # 插入空列[3,6](@ref)
df_main.insert(insert_pos, '真实销售额', real_sales)  # 插入计算列[1,7](@ref)


# 合并商品简称（左连接避免数据丢失）
df_main = df_main.merge(
    df_mapping[['商品ID', '商品简称']],
    on='商品ID',
    how='left'
)  # [2,8](@ref)

# 调整列顺序：将商品简称插入到商品ID列之后
cols = df_main.columns.tolist()
cols.insert(cols.index('商品ID')+1, cols.pop(cols.index('商品简称')))
df_main = df_main[cols]  # [4](@ref)

df_main = df_main.dropna(subset=['商品简称'])
# 保存处理后的数据

df_main.to_excel("../data/howgo数据/"+current_date+"周报数据.xlsx", index=False, engine='openpyxl')  # [5,10](@ref)
print(df_main)