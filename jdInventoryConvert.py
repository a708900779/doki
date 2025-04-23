import pandas as pd
import numpy as np


Store_Data_PATH = 'data/京东库存0326.xlsx'

cityList = ['杭州','深圳','北京','武汉','成都','沈阳','西安']

prductCodeList = ['EMG4418152092014','EMG4418210447469','EMG4418212367632','EMG4418208889030','EMG4418416908906','EMG4418422384339',
'EMG4418254273209','EMG4418279176732','EMG4418531683543','EMG4418535776876']


# 读取文件，文件编码是gbk类型
storeData = pd.read_excel(Store_Data_PATH)
# 设置索引
t1 = pd.DataFrame(storeData)
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



