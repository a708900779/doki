
output = []

matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [5, 6, 7, 8],
    [5, 6, 7, 8],
    [5, 6, 7, 8],
    [5, 6, 7, 8],
    [5, 6, 7, 8],
    [5, 6, 7, 8],
    [5, 6, 7, 8],
    [5, 6, 7, 8],
    # ... 其他9行数据
]
def array_to_string(arr):
    result = []
    for idx, row in enumerate(arr):
        # 列间用Tab分隔，行末尾添加换行符
        line = '\t'.join(map(str, row))
        # 判断是否为第六行或第八行（索引5或7）
        if idx + 1 in [6, 8]:
            line += '\n\n'  # 额外添加一个换行符
        else:
            line += '\n'
        result.append(line)
    return ''.join(result).strip()  # 最后去除末尾多余的换行

print(array_to_string(matrix))

