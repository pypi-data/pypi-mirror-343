from tpltable.core import *

# 定义样式类型常量
TYPE_COLOR = "t_color"  # 前景色
TYPE_BCOLOR = "t_bcolor"  # 背景色
TYPE_FONT_TYPE = "t_font_type"  # 字体
TYPE_FONT_SIZE = "t_font_size"  # 字号
TYPE_FONT_BOLD = "t_font_bold"  # 粗体
TYPE_FONT_ITALIC = "t_font_italic"  # 斜体
TYPE_UNDERLINE = "t_underline"  # 下划线
TYPE_DELETE_LINE = "t_delete_line"  # 删除线
TYPE_HALIGN = "t_halign"  # 水平对齐
TYPE_VALIGN = "t_valign"  # 垂直对齐
TYPE_BORDER = "t_border"  # 边框
TYPE_ROW_HEIGHT = "t_row_height"  # 行高
TYPE_COL_WIDTH = "t_col_width"  # 列宽
TYPE_DATA_FORMAT = "t_data_format"  # 数据格式
TYPE_AUTO_NEWLINE = "t_auto_newline"  # 自动换行
_STYLE_TYPES = [
    TYPE_COLOR, TYPE_BCOLOR, TYPE_FONT_TYPE, TYPE_FONT_SIZE, TYPE_FONT_BOLD, TYPE_FONT_ITALIC,
    TYPE_UNDERLINE, TYPE_DELETE_LINE, TYPE_HALIGN, TYPE_VALIGN, TYPE_ROW_HEIGHT, TYPE_COL_WIDTH, TYPE_DATA_FORMAT, TYPE_AUTO_NEWLINE
]
F_STRING = '@'  # 文本格式
F_NUMBER = '0'  # 数字格式，无小数点
F_DATE = 'YYYY-MM-DD'  # 日期格式，示例为年-月-日
F_TIME = 'HH:MM:SS'  # 时间格式，示例为时:分:秒

_DEFAULT_STYLE = {
    TYPE_COLOR: 1, TYPE_BCOLOR: '00000000',
    TYPE_BORDER: {
        'left': {'style': None, 'color': None, 'border_style': None},
        'right': {'style': None, 'color': None, 'border_style': None},
        'top': {'style': None, 'color': None, 'border_style': None},
        'bottom': {'style': None, 'color': None, 'border_style': None},
        'diagonal': {'style': None, 'color': None, 'border_style': None},
        'diagonal_direction': None,
        'vertical': None, 'horizontal': None,
        'diagonalUp': False, 'diagonalDown': False,
        'outline': True, 'start': None, 'end': None
    },
    TYPE_FONT_TYPE: 'Calibri', TYPE_FONT_SIZE: 11.0,
    TYPE_FONT_BOLD: False, TYPE_FONT_ITALIC: False,
    TYPE_UNDERLINE: False, TYPE_DELETE_LINE: None,
    TYPE_HALIGN: None, TYPE_VALIGN: None,
    TYPE_ROW_HEIGHT: None, TYPE_COL_WIDTH: 13.0,
    TYPE_DATA_FORMAT: 'General',
    TYPE_AUTO_NEWLINE: None
}

COLOR_BLACK = '00000000'
COLOR_WHITE = '00FFFFFF'
COLOR_RED = '00FF0000'
COLOR_DARKRED = '00800000'
COLOR_LIGHTRED = '00FFC0CB'
COLOR_BLUE = '000000FF'
COLOR_DARKBLUE = '00000080'
COLOR_LIGHTBLUE = '00ADD8E6'
COLOR_GREEN = '0000FF00'
COLOR_DARKGREEN = '00008000'
COLOR_LIGHTGREEN = '0098FB98'
COLOR_YELLOW = '00FFFF00'
COLOR_DARKYELLOW = '00808000'
COLOR_LIGHTYELLOW = '00FFFFE0'
COLOR_ORANGE = '00FFA500'
COLOR_DARKORANGE = '00FF8C00'
COLOR_LIGHTORANGE = '00FFD700'
COLOR_PURPLE = '00800080'
COLOR_DARKPURPLE = '00800080'
COLOR_LIGHTPURPLE = '00E6E6FA'
COLOR_GRAY = '00808080'
COLOR_DARKGRAY = '00808080'
COLOR_LIGHTGRAY = '00D3D3D3'
COLOR_CYAN = '0000FFFF'
COLOR_DARKCYAN = '00008080'
COLOR_LIGHTCYAN = '00E0FFFF'
COLOR_MAGENTA = '00FF00FF'
COLOR_DARKMAGENTA = '00800080'
COLOR_LIGHTMAGENTA = '00FFC0CB'

SIDE_THIN_BLACK = Side(style='thin', color=COLOR_BLACK)

BORDER_LTRB = Border(SIDE_THIN_BLACK, SIDE_THIN_BLACK, SIDE_THIN_BLACK, SIDE_THIN_BLACK)
BORDER_NOLEFT = Border(None, SIDE_THIN_BLACK, SIDE_THIN_BLACK, SIDE_THIN_BLACK)
BORDER_NORIGHT = Border(SIDE_THIN_BLACK, None, SIDE_THIN_BLACK, SIDE_THIN_BLACK)
BORDER_NOTOP = Border(SIDE_THIN_BLACK, SIDE_THIN_BLACK, None, SIDE_THIN_BLACK)
BORDER_NOBOTTOM = Border(SIDE_THIN_BLACK, SIDE_THIN_BLACK, SIDE_THIN_BLACK, None)
BORDER_LT = Border(SIDE_THIN_BLACK, SIDE_THIN_BLACK, None, None)
BORDER_RB = Border(None, None, SIDE_THIN_BLACK, SIDE_THIN_BLACK)
BORDER_LB = Border(SIDE_THIN_BLACK, None, None, SIDE_THIN_BLACK)
BORDER_RT = Border(None, SIDE_THIN_BLACK, SIDE_THIN_BLACK, None)
BORDER_LR = Border(SIDE_THIN_BLACK, SIDE_THIN_BLACK, None, None)
BORDER_TB = Border(None, None, SIDE_THIN_BLACK, SIDE_THIN_BLACK)
BORDER_L = Border(SIDE_THIN_BLACK, None, None, None)
BORDER_R = Border(None, SIDE_THIN_BLACK, None, None)
BORDER_T = Border(None, None, SIDE_THIN_BLACK, None)
BORDER_B = Border(None, None, None, SIDE_THIN_BLACK)


def _GetCellStyle(ws, cell, style_type: str) -> object:
    if style_type == TYPE_COLOR:
        return cell.font.color
    elif style_type == TYPE_BCOLOR:
        return cell.fill.fgColor
    elif style_type == TYPE_FONT_TYPE:
        return cell.font.name
    elif style_type == TYPE_FONT_SIZE:
        return cell.font.size
    elif style_type == TYPE_FONT_BOLD:
        return cell.font.bold
    elif style_type == TYPE_FONT_ITALIC:
        return cell.font.italic
    elif style_type == TYPE_UNDERLINE:
        return cell.font.underline == 'single'
    elif style_type == TYPE_DELETE_LINE:
        return cell.font.strikethrough
    elif style_type == TYPE_HALIGN:
        return cell.alignment.horizontal
    elif style_type == TYPE_VALIGN:
        return cell.alignment.vertical
    elif style_type == TYPE_AUTO_NEWLINE:
        return cell.alignment.wrapText
    elif style_type == TYPE_BORDER:
        return cell.border
    elif style_type == TYPE_ROW_HEIGHT:
        return ws.row_dimensions[cell.row].height  # 获取行高(Strange, why not tc.cell.row_dimensions is same as tc.cell.column_dimensions? One is str, the other is int.)
    elif style_type == TYPE_COL_WIDTH:
        col_letter = get_column_letter(cell.column)
        return ws.column_dimensions[col_letter].width  # 获取列宽
    elif style_type == TYPE_DATA_FORMAT:
        return cell.number_format
    else:
        raise ValueError(f"Unknown style type: {style_type}")


def _SetCellStyle(ws, cell, style_type: str, value):
    # 先保存当前的样式，以便我们可以修改并重新应用
    current_font = cell.font
    current_alignment = cell.alignment
    new_font = copy(current_font)  # 使用copy来创建一个可修改的副本
    new_alignment = copy(current_alignment)  # 使用copy来创建一个可修改的副本

    if style_type == TYPE_COLOR:
        new_font.color = value
    elif style_type == TYPE_BCOLOR:
        cell.fill = PatternFill(fgColor=value, bgColor=value, fill_type='solid')
    elif style_type == TYPE_FONT_TYPE:
        new_font.name = value
    elif style_type == TYPE_FONT_SIZE:
        new_font.size = value
    elif style_type == TYPE_FONT_BOLD:
        new_font.bold = value
    elif style_type == TYPE_FONT_ITALIC:
        new_font.italic = value
    elif style_type == TYPE_UNDERLINE:
        if value:
            new_font.underline = 'single'
        else:
            new_font.underline = None
    elif style_type == TYPE_DELETE_LINE:
        new_font.strikethrough = value
    elif style_type == TYPE_HALIGN:
        new_alignment.horizontal = value
    elif style_type == TYPE_VALIGN:
        new_alignment.vertical = value
    elif style_type == TYPE_AUTO_NEWLINE:
        new_alignment.wrapText = value
    elif style_type == TYPE_BORDER:
        cell.border = value
    elif style_type == TYPE_ROW_HEIGHT:
        ws.row_dimensions[cell.row].height = value  # 设置行高
    elif style_type == TYPE_COL_WIDTH:
        # 将数字索引转换为列字母标识
        col_letter = get_column_letter(cell.column)
        ws.column_dimensions[col_letter].width = value  # 设置列宽
    elif style_type == TYPE_DATA_FORMAT:
        cell.number_format = value  # 设置数据格式
    else:
        raise ValueError(f"Unknown style type: {style_type}")

    # 重新应用修改后的样式
    cell.font = new_font
    cell.alignment = new_alignment


class Style:
    def __init__(self, ws: Worksheet, cell: Cell, *, copy_mode:bool=False):
        if copy_mode:  # ws is {} and cell is ()
            assert isinstance(ws, dict) and isinstance(cell, tuple), "Copy mode must be used with dict and tuple."
            self._styles = ws
            self._source = cell
            return

        _style_dict = {}
        for style_type in _STYLE_TYPES:
            _style_dict[style_type] = _GetCellStyle(ws, cell, style_type)

        self._styles: dict = _style_dict

        # NOTE: border is a special case
        _bd = _GetCellStyle(ws, cell, TYPE_BORDER)
        if _bd is not None:
            # def __init__(self, left=None, right=None, top=None,
            #              bottom=None, diagonal=None, diagonal_direction=None,
            #              vertical=None, horizontal=None, diagonalUp=False, diagonalDown=False,
            #              outline=True, start=None, end=None):
            self._styles[TYPE_BORDER] = Border(
                left=_bd.left, right=_bd.right, top=_bd.top, bottom=_bd.bottom,
                diagonal=_bd.diagonal, diagonal_direction=_bd.diagonal_direction,
                vertical=_bd.vertical, horizontal=_bd.horizontal,
                diagonalUp=_bd.diagonalUp, diagonalDown=_bd.diagonalDown,
                outline=_bd.outline, start=_bd.start, end=_bd.end
            )

        self._source = (ws.title, cell.coordinate)

    def __getitem__(self, style_type: str):
        return self._styles[style_type]

    def __setitem__(self, style_type: str, value):
        if style_type is TYPE_COLOR:
            value = Color(value)
        self._styles[style_type] = value

    def __repr__(self):
        return f"Style{self._source}"

    def __str__(self):
        _txt = f"Style{self._source}\t" + '{\n'
        for key, value in self._styles.items():
            _txt += f"\t'{key}': {value},\n"
        _txt += '}'
        return _txt

    def __is_default_style_item(self, type_key, test_value) -> bool:
        if type_key == TYPE_COLOR:
            if isinstance(test_value, Color):
                return test_value.value == _DEFAULT_STYLE[TYPE_COLOR]
            return test_value == _DEFAULT_STYLE[TYPE_COLOR]
        elif type_key == TYPE_BCOLOR:
            if isinstance(test_value, Color):
                return test_value.value == _DEFAULT_STYLE[TYPE_BCOLOR]
            return test_value == _DEFAULT_STYLE[TYPE_BCOLOR]
        elif type_key == TYPE_BORDER:
            if isinstance(test_value, Border):
                return self.__get_border_dict(test_value) == _DEFAULT_STYLE[TYPE_BORDER]
            return test_value == _DEFAULT_STYLE[TYPE_BORDER]
        else:
            return test_value == _DEFAULT_STYLE[type_key]


    def __get_border_dict(self, _bd:Border=None) -> Union[dict, None]:
        _bd = self._styles.get(TYPE_BORDER) if _bd is None else _bd
        if _bd is not None:
            # Side:
            # def __init__(
            #         self,
            #         style: _SideStyle | Literal["none"] | None = None,
            #         color: str | Color | None = None,
            #         border_style: Incomplete | None = None,
            _l, _r, _t, _b, _diag = _bd.left, _bd.right, _bd.top, _bd.bottom, _bd.diagonal
            return {
                'left': {'style': _l.style, 'color': _l.color, 'border_style': _l.border_style} if _l is not None else None,
                'right': {'style': _r.style, 'color': _r.color, 'border_style': _r.border_style} if _r is not None else None,
                'top': {'style': _t.style, 'color': _t.color, 'border_style': _t.border_style} if _t is not None else None,
                'bottom': {'style': _b.style, 'color': _b.color, 'border_style': _b.border_style} if _b is not None else None,
                'diagonal': {'style': _diag.style, 'color': _diag.color, 'border_style': _diag.border_style} if _diag is not None else None,
                'diagonal_direction': _bd.diagonal_direction,
                'vertical': _bd.vertical, 'horizontal': _bd.horizontal,
                'diagonalUp': _bd.diagonalUp, 'diagonalDown': _bd.diagonalDown,
                'outline': _bd.outline, 'start': _bd.start, 'end': _bd.end
            }
        return None

    def apply(self, ws: Worksheet, cell: Cell):
        for style_type, value in self._styles.items():
            if self.__is_default_style_item(style_type, value):
                continue
            _SetCellStyle(ws, cell, style_type, value)

    @staticmethod
    def color(r_cstr: Union[str, int], g: int = None, b: int = None) -> str:
        if isinstance(r_cstr, str):
            r_cstr = r_cstr.upper().strip()
            if r_cstr.startswith('#'):
                r_cstr = r_cstr[1:]
            if len(r_cstr) != 6:
                raise ValueError("Color string must be 6 characters long")
            return '00' + r_cstr
        else:
            if g is None or b is None:
                raise ValueError("Color value must be RGB")
            return f'00{r_cstr:02X}{g:02X}{b:02X}'

    def todict(self) -> dict:
        # return self._styles.copy()
        _ = {
            TYPE_COLOR: self._styles[TYPE_COLOR].value if self._styles.get(TYPE_COLOR) is not None else COLOR_BLACK,
            TYPE_BCOLOR: self._styles[TYPE_BCOLOR].value if self._styles.get(TYPE_BCOLOR) is not None else COLOR_WHITE,
            TYPE_BORDER: self.__get_border_dict(),
        }
        OTHER_KEYS = _STYLE_TYPES.copy()
        OTHER_KEYS.remove(TYPE_COLOR)
        OTHER_KEYS.remove(TYPE_BCOLOR)

        for key in OTHER_KEYS:
            _[key] = self._styles.get(key)
            if key == TYPE_BORDER:
                continue
        return _

    def copy(self):
        return Style(self._styles.copy(), self._source, copy_mode=True)

    @staticmethod
    def Default() -> object:
        return _DEFAULT

    def set(self, key:str, value:object):
        self[key] = value





def _raw_style() -> Style:
    wb = Workbook()
    ws = wb.active
    cell = ws['A1']
    cell.value = 'Hello, World!'
    return Style(ws, cell)

___ = Workbook().active
___ = ___, ___['A1']
___[1].value = 0
_DEFAULT = Style(___[0], ___[1])
del ___

if __name__ == '__main__':
    rs = _raw_style()
    rsd = rs.todict()
    print(rsd)
