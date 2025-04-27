from tpltable.excel import Excel, Table
from tpltable.style import *

e = Excel()

# t = e.append(Table(
#     [[0],
#     [4, 5, 6, 7],
#     [8, 9, 10, 11],
#     [12, 13, 14, 15]])
# )
#
# t.styles.set(TYPE_HALIGN, 'center')  # 设置水平居中
# t.styles['A2', 'D3'].set(TYPE_COLOR, 'FF0000')  # 设置红色前景色
# t.styles['A:D'].set(TYPE_FONT_TYPE, 'Arial')  # 设置字体
# t.styles['A1:D4'].set(TYPE_FONT_SIZE, 20)  # 设置字号
# t.styles['A1'].set(TYPE_COL_WIDTH, 40)  # 设置列宽
# t.styles[:, 1].set(TYPE_BCOLOR, COLOR_LIGHTGRAY)  # 设置浅灰色背景色
# t.merge("A1:D1")  # 合并单元格
#
# print(S
#     e.detail()
# )

t = e.append(Table())

t.append(
    [1, 2, 3, 4, 10],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
)

t.merge('A1:F2')
t.merge('E2:H3')
print(t)

e.save('test.xlsx')






