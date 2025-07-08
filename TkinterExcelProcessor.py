import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np


class ExcelProcessorApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("京东数据表处理")
        self.window.geometry("600x400")

        # 文件选择按钮
        self.btn_select = tk.Button(self.window, text="选择Excel文件", command=self.select_file)
        self.btn_select.pack(pady=20)

        # 结果显示区域（支持滚动）
        self.text_output = tk.Text(self.window, height=15, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(self.window, command=self.text_output.yview)
        self.text_output.configure(yscrollcommand=scrollbar.set)
        self.text_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")]
        )
        if file_path:
            try:
                # 调用现有数据处理代码（需替换为你的逻辑）
                df = pd.read_excel(file_path)
                result = self.process_data(df)  # 假设这是你的处理函数
                self.text_output.delete(1.0, tk.END)
                self.text_output.insert(tk.END, result)
            except Exception as e:
                messagebox.showerror("错误", f"文件处理失败：{str(e)}")

    def process_data(self, df):
        # 示例：假设这是你的数据处理逻辑
        cityList = ['杭州', '深圳', '北京', '武汉', '成都', '沈阳', '西安']

        prductCodeList = ['EMG4418152092014', 'EMG4418210447469', 'EMG4418212367632', 'EMG4418208889030',
                          'EMG4418416908906', 'EMG4418422384339',
                          'EMG4418254273209', 'EMG4418279176732', 'EMG4418792349011', 'EMG4418531683543',
                          'EMG4418535776876', 'EMG4418731721033', 'EMG4418811201244', 'EMG4418731720841',
                          'EMG4418749905666', 'EMG4418749906650','EMG4418279175564', 'EMG4418417149542',
                          'EMG4418791451639']

        # 读取文件，文件编码是gbk类型
        storeData = df
        # 设置索引
        t1 = pd.DataFrame(storeData)
        # 创建最终结果 二维数组
        resultArray = np.zeros((len(cityList), len(prductCodeList)))

        cityTimes = 0
        # 根据仓库名筛选
        for city in cityList:
            cityTable = t1[t1['仓库名称'].str.contains(city) == True]
            cityDict = dict()
            for index, row in cityTable.iterrows():
                productCode = row['事业部商品编码']
                if not productCode in cityDict:
                    cityDict.setdefault(productCode, row['可用库存'])
                else:
                    num = cityDict.get(productCode)
                    finalNum = num + row['可用库存']
                    cityDict[productCode] = finalNum
            productTimes = 0
            for productCode in prductCodeList:
                if cityDict.get(productCode) != None:
                    resultArray[cityTimes, productTimes] = cityDict.get(productCode)
                else:
                    resultArray[cityTimes, productTimes] = 0
                productTimes = productTimes + 1
            cityTimes = cityTimes + 1
        resultArray = np.transpose(resultArray)
        return array_to_string(resultArray)

    def run(self):
        self.window.mainloop()


def array_to_string(arr):
    # 辅助函数：将数值类型转换为无小数点的字符串
    def convert_element(x):
        if isinstance(x, (int, float)):
            return str(int(x))  # 直接取整（截断小数）
        else:
            return str(x)

    result = []
    for idx, row in enumerate(arr):
        # 1. 处理每个元素，确保数值不带小数点
        processed_row = [convert_element(e) for e in row]

        # 2. 用Tab拼接列，行末添加换行符
        line = '\t'.join(processed_row)

        # 3. 判断是否为第六行或第八行（逻辑行号，从1开始）
        if idx + 1 in [6, 9,11,14,16]:
            line += '\n\n'  # 添加两个换行符
        else:
            line += '\n'  # 普通行添加一个换行符

        result.append(line)

    # 合并结果并去除末尾多余换行
    return ''.join(result).strip()

if __name__ == "__main__":
    app = ExcelProcessorApp()
    app.run()


