import chardet as chardet
import pandas as pd
import numpy as np
import openpyxl



#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)

Store_Data_PATH = 'data/京东库存0326.xlsx'
Result_Data_PATH = 'data/京东库存.xlsx'



cityList = ['杭州','深圳','北京','武汉','成都','沈阳','西安']

prductCodeList = ['EMG4418152092014','EMG4418210447469','EMG4418212367632','EMG4418208889030','EMG4418416908906','EMG4418422384339',
'EMG4418254273209','EMG4418279176732','EMG4418531683543','EMG4418535776876']




# 读取文件，文件编码是gbk类型
storeData = pd.read_excel(Store_Data_PATH)

# 设置索引
t1 = pd.DataFrame(storeData)

# # 删除库存为0的 数据
# t1 = t1.drop(t1[t1['总库存'] == 0].index)
# # 删除 残次品
# t1 = t1.drop(t1[t1['库存状态'] != '良品'].index)

# 删除 无关列
# t1 = t1.drop(['序号','仓库编码','事业部商品名称','商家商品编码','库存状态','库存类型','商家商品标识','商品等级编码','可用库存','事业部编码','事业部名称','计量单位','款号','颜色','尺寸','季节','年份'],axis=1)
# t1 = t1.drop(['仓库编码','事业部商品名称','商家商品编码','商家商品标识',,'事业部编码','事业部名称','计量单位','年份'],axis=1)

# t1 = t1.drop(['仓库编码','事业部商品名称','商家商品编码','商家商品标识','事业部编码','事业部名称','计量单位'],axis=1)



# 创建最终结果 二维数组
resultArray = np.zeros((len(cityList),len(prductCodeList)))

cityTimes = 0
# 根据仓库名筛选
for city in cityList:
    cityTable = t1[t1['仓库名称'].str.contains(city) == True]
    cityDict = dict()
    for index,row in cityTable.iterrows():
        productCode = row['事业部商品编码']
        if not productCode in cityDict:
            cityDict.setdefault(productCode, row['可用库存'])
        else:
            num = cityDict.get(productCode)
            finalNum = num + row['可用库存']
            cityDict[productCode] = finalNum
    cityNumList = []
    productTimes = 0
    for productCode in prductCodeList:
        if cityDict.get(productCode) != None:
            resultArray[cityTimes, productTimes] = cityDict.get(productCode)
        else:
            resultArray[cityTimes, productTimes] = 0
        productTimes = productTimes +1
    cityTimes = cityTimes + 1


for j in range(len(prductCodeList)):
    if(j == 6):
        print()
    if(j == 8):
        print()
    for i in range(len(cityList)):
        print( "%d" %(resultArray[i][j]),end='\t')
    print()


def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']



