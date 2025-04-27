from tpltable.excel import Excel
from tpltable.style import Style
from tpltable.table import Table, Row, Col
from tpltable.core import Coord, isnan, NaN


if __name__ == '__main__':
    from tpltable.style import TYPE_HALIGN, TYPE_COLOR, TYPE_FONT_TYPE, TYPE_FONT_SIZE, TYPE_COL_WIDTH, TYPE_BCOLOR, COLOR_LIGHTGRAY
    e = Excel()

    t = e.append(Table(
        [[0],
        [4, 5, 6, 7],
        [8, 9, 10, 11],
        [12, 13, 14, 15]])
    )

    t.styles.set(TYPE_HALIGN, 'center')  # 设置水平居中
    t.styles['A2', 'D3'].set(TYPE_COLOR, 'FF0000')  # 设置红色前景色
    t.styles['A:D'].set(TYPE_FONT_TYPE, 'Arial')  # 设置字体
    t.styles['A1:D4'].set(TYPE_FONT_SIZE, 20)  # 设置字号
    t.styles['A1'].set(TYPE_COL_WIDTH, 40)  # 设置列宽
    t.styles[:, 1].set(TYPE_BCOLOR, COLOR_LIGHTGRAY)  # 设置浅灰色背景色
    t.merge("A1:D1")  # 合并单元格

    # e.save('test.xlsx')

    del t['A']

    del t['B1', 'C2']

    e.save('test.xlsx')

