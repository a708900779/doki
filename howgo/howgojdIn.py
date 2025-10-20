import pandas as pd
import numpy as np
from datetime import datetime

now = datetime.now()
month = str(now.month).zfill(2)  # 月份补零
day = str(now.day).zfill(2)      # 日期补零
current_date = month + day

Store_Data_PATH = "../data/howgo京东库存/采购工作台已下发信息列表"+current_date+".xlsx"

cityList = ['上海','肇庆','北京','武汉','成都','沈阳','西安']

prductCodeList = ['EMG4418741184766','EMG4418741188310','EMG4418746662661','EMG4418746726633','EMG4418826143784','EMG4418746668905',
'EMG4418826148944','EMG4418805866471','EMG4418849268764','EMG4418769786105','EMG4418849269976','EMG4418849270028','EMG4418849270132'
,'EMG4418860718520'
,'EMG4418817319483'
,'EMG4418781237253'
,'EMG4418817319611'
,'EMG4418860721488'
,'EMG4418775767954'
,'EMG4418775768026'
,'EMG4418775768078'
,'EMG4418899429367'
]


# 读取文件，文件编码是gbk类型
storeData = pd.read_excel(Store_Data_PATH)
# 设置索引
t1 = pd.DataFrame(storeData)
# 创建最终结果 二维数组
resultArray = np.zeros((len(cityList),len(prductCodeList)))

cityTimes = 0
# 根据仓库名筛选
for city in cityList:
    cityTable = t1[t1['入库库房名称'].str.contains(city) == True]
    cityDict = dict()
    for index,row in cityTable.iterrows():
        productCode = row['商品编码']
        if not productCode in cityDict:
            cityDict.setdefault(productCode, row['采购量'])
        else:
            num = cityDict.get(productCode)
            finalNum = num + row['采购量']
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
    if(j == 7):
        print()
    if(j == 13):
        print()
    for i in range(len(cityList)):
        print( "%d" %(resultArray[i][j]),end='\t')
    print()



