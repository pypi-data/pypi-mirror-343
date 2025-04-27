import numpy as np
import pandas as pd
from tpltable.table import *
from tpltable.style import *


class ListkeysDict(dict):
    _DEFAULT_PREFIX = "NAME_"

    def __init__(self, value=None, *, keys: list = None):
        if value is None:
            value = {}
        super().__init__(value)
        self._keys = list(super().keys())

        if keys is not None:
            for k in keys:
                if k not in self:
                    raise KeyError(f"Unknown key:{k} from custom keys")

            for k in self:
                if k not in keys:
                    raise KeyError(f"Mising key:{k} from custom keys")

            self._keys = list(keys)

        self._last_key_number = 0

    def _generate_key(self):
        """生成一个唯一的键名，确保不与现有键冲突。"""
        self._last_key_number += 1
        key = f"{self._DEFAULT_PREFIX}{self._last_key_number}"
        while key in self:
            key = '_' + key
        return key

    def _get_keys(self, key) -> list:
        try:
            if isinstance(key, slice):
                return self._keys[key]
            elif isinstance(key, int):
                return [self._keys[key]]
            else:
                return [key]
        except IndexError:
            raise KeyError(f"Key:{key} is out of bound.")

    # Note: Dicts: ..........................................................................
    def keys(self):
        return self._keys.copy()

    def values(self):
        return [self[k] for k in self._keys]

    def items(self):
        return [(k, self[k]) for k in self._keys]

    def get(self, key, default=None):
        if isinstance(key, int):
            key = self._keys[key]
        elif isinstance(key, str):
            key = key
        else:
            raise TypeError(f"unexpected key type:{type(key)}.")
        return super().get(key, default)

    def update(self, _m):
        for k, v in _m.items():
            if k not in self:
                self._keys.append(k)
            super().__setitem__(k, v)

    @classmethod
    def fromkeys(cls, keys, value=None):
        return cls({k: value for k in keys})

    def setdefault(self, __key, __default = None):
        if __key not in self:
            self._keys.append(__key)
        return super().setdefault(__key, __default)

    def popitem(self):
        key = self._keys.pop()
        return key, super().pop(key)


    # Note: Lists: ..........................................................................

    def append(self, value, *, key: str = None):
        """在列表末尾添加元素。"""
        if key is None:
            key = self._generate_key()
        if key in self:
            raise KeyError(f"Repeat key: {key}")
        self._keys.append(key)
        super().__setitem__(key, value)

    def extend(self, _m):
        for k, v in _m.items():
            if k not in self:
                self._keys.append(k)
            super().__setitem__(k, v)

    def insert(self, index, value, *, key: str = None):
        """在指定位置插入元素。"""
        if index > len(self):
            raise IndexError("Index out of range.")
        if key is None:
            key = self._generate_key()
        if isinstance(index, str):
            index = self._keys.index(index)

        if key in self:
            raise KeyError(f"Repeat key: {key}")

        # self[key] = value
        super().__setitem__(key, value)
        self._keys.insert(index, key)


    def index(self, value, start=0, stop=EMPTY_INDEX):
        if stop is EMPTY_INDEX:
            stop = len(self)
        for i, k in enumerate(self._keys[start:stop]):
            if self[k] == value:
                return i
        raise ValueError(f"{value} is not in listkeys_dict.")

    def remove(self, value):
        i = self.index(value)
        super().__delitem__(self._keys[i])
        self._keys.pop(i)

    def reverse(self):
        self._keys.reverse()

    def sort(self, key=None, reverse=False):
        if key is None:
            key = lambda x: x
        self._keys.sort(key=lambda x: key(super().__getitem__(x)), reverse=reverse)

    def count(self, value):
        return sum([1 for k in self._keys if super().__getitem__(k) == value])

    # Note: Both Dicts & Lists: ..........................................................................
    def pop(self, key, default=EMPTY_INDEX):
        keys = self._get_keys(key)

        for key in keys:
            if default is EMPTY_INDEX:
                return super().pop(key)
            else:
                return super().pop(key, default)


    def clear(self):
        self._keys.clear()
        super().clear()

    def copy(self):
        return ListkeysDict(self, keys=self._keys.copy())


    def __getitem__(self, key):
        keys = self._get_keys(key)

        _ret = []
        for key in keys:
            _ret.append(super().__getitem__(key))

        if len(_ret) == 1:
            return _ret[0]
        return _ret

    def __setitem__(self, key, value):
        keys = self._get_keys(key)

        for key in keys:
            if key not in self:
                self._keys.append(key)
            super().__setitem__(key, value)

    def __delitem__(self, key):
        keys = self._get_keys(key)

        for key in keys:
            super().__delitem__(key)
            self._keys.remove(key)

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self._keys)


    def __str__(self):
        """提供字典内容的字符串表示。"""
        txt = "{"
        for i, (k, v) in enumerate(self.items()):
            if isinstance(k, str):
                k = f"'{k}'"
            if isinstance(v, str):
                v = f"'{v}'"

            txt += f"{i}|{k}: {v}, "

        if txt[-1] != '{':
            txt = txt[:-2]

        return txt + '}'

    def __repr__(self):
        return str(self)

    # MATH
    def __add__(self, other):
        if isinstance(other, ListkeysDict):
            return ListkeysDict({**self, **other})
        return NotImplemented

    def __radd__(self, other: dict):
        other.update(self)
        return other

    def __iadd__(self, other):
        self.update(other)
        return self

    def __sub__(self, other):
        if isinstance(other, ListkeysDict):
            return ListkeysDict({k: v for k, v in self.items() if k not in other})
        return NotImplemented

    def __rsub__(self, other: dict):
        return {k: v for k, v in other.items() if k not in self}

    def __isub__(self, other):
        for k in other:
            self.pop(k, None)
        return self

    def __mul__(self, other):
        raise TypeError("unsupported operand type(s) for *: 'ListkeysDict' and 'int'")

    def __rmul__(self, other):
        raise TypeError("unsupported operand type(s) for *: 'int' and 'ListkeysDict'")

    def __imul__(self, other):
        raise TypeError("unsupported operand type(s) for *: 'ListkeysDict' and 'int'")

    # COMPARE
    def __eq__(self, other):
        if isinstance(other, dict):
            _items0, _items1 = self.items(), other.items()
            return _items0 == _items1

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        raise TypeError("unorderable types: 'ListkeysDict' < 'ListkeysDict'")

    def __le__(self, other):
        raise TypeError("unorderable types: 'ListkeysDict' <= 'ListkeysDict'")

    def __gt__(self, other):
        raise TypeError("unorderable types: 'ListkeysDict' > 'ListkeysDict'")

    def __ge__(self, other):
        raise TypeError("unorderable types: 'ListkeysDict' >= 'ListkeysDict'")

    # TYPE
    def __bool__(self):
        return bool(self._keys)

    def __contains__(self, item):
        return item in self._keys

    def __hash__(self):
        raise TypeError("unhashable type: 'ListkeysDict'")


def test_listkeys_dict():
    # 创建listkeys_dict实例
    d = ListkeysDict()

    # 测试append方法
    d.append('apple')
    d.append('banana')
    print("After appends:", d)  # 应显示：['XXX1', 'XXX0'] = ['apple', 'banana']

    # 测试getitem方法
    print("Get item by int index 0:", d[0])  # 应显示：'XXX0'
    print("Get item by int index 1:", d[1])  # 应显示：'XXX1'

    # 测试setitem方法
    d[1] = 'cherry'
    print("After setting item 1 to 'cherry':", d)  # 应显示：['XXX0', 'XXX_XXX1'] = ['apple', 'cherry']

    # 测试delitem方法
    del d[0]
    print("After deleting item 0:", d)  # 应显示：['XXX_XXX1'] = ['cherry']

    # 测试insert方法
    d.insert(0, 'date')
    print("After inserting 'date' at index 0:", d)  # 应显示：['XXX2', 'XXX_XXX1'] = ['date', 'cherry']

    # 测试迭代
    print("Iterating over keys:", list(d))  # 应显示：['XXX2', 'XXX_XXX1']

    # 测试长度
    print("Length of d:", len(d))  # 应显示：2

    # 测试切片
    print("Slice of d:", d[0:2])  # 应显示：['XXX2', 'XXX_XXX1']

    # 测试生成key
    print("Generated key:", d._generate_key())  # 应显示一个唯一的key

    # 测试异常处理
    try:
        d['nonexistent']
    except KeyError as e:
        print("Caught an exception:", e)

    try:
        del d[10]
    except KeyError as e:
        print("Caught an exception:", e)

    try:
        d[10] = 'mystery'
    except KeyError as e:
        print("Caught an exception:", e)


class ExcelFileIOException(Exception):
    pass


class Excel(ListkeysDict):
    _DEFAULT_PREFIX = 'Sheet'
    def __init__(self, fpath: str = None, *, style: bool = True):
        """
        *Create an Excel object from an excel file or empty
        :param fpath: excel file path. If None, will create an empty Excel object.
        *
        :param style: bool. If True, will load the style of the cell(may be cost). Default is True.
        """
        self._path = fpath
        if self._path:
            # try:
            wb = load_workbook(fpath)
            tbls = {sheet.title: self.__table_from_sheet(sheet, only_data=not style) for sheet in wb.worksheets}
            wb.close()
        # except Exception as e:
        #     raise ExcelFileIOException("\n\nFatal to load excel file: \n" + reinsert_indent(str(e), '\t'))
        else:
            tbls = {}

        super().__init__(tbls)

    def __getitem__(self, item):
        if isinstance(item, tuple):
            _i0 = item[0]
            item = item[1:] if len(item) >= 2 else None
        else:
            _i0 = item
            item = None

        if item is None:
            return super().__getitem__(_i0)
        return super().__getitem__(_i0)[item]

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            _i0 = key[0]
            item = key[1:] if len(key) >= 2 else None
        else:
            _i0 = key
            key = None

        if key is None:
            assert isinstance(value, Table), f"Unexpected Table type:{value}"

        if item is None:
            super().__setitem__(_i0, value)
            return
        super().__getitem__(_i0)[item] = value

    def __delitem__(self, key):
        if isinstance(key, tuple):
            _i0 = key[0]
            key = key[1:] if len(key) >= 2 else None
        else:
            _i0 = key
            key = None

        super().__delitem__(key)

    def __table_from_sheet(self, sheet: Worksheet, only_data: bool = False):
        _construct_2d_list = []
        _merges = [_merge.coord for _merge in sheet.merged_cells.ranges]

        if only_data:
            _styles = None
            for row in sheet.iter_rows():
                _construct_2d_list.append([cell.value if cell.value else NaN for cell in row])
        else:
            _styles = []
            for row in sheet.iter_rows():
                _construct_2d_list.append([cell.value if cell.value else NaN for cell in row])
                _styles.append([Style(sheet, cell) for cell in row])

        return Table(_construct_2d_list, _styles, _merges, copy=False)

    @property
    def path(self):
        return self._path

    @property
    def tables(self):
        return list(self.values())

    @staticmethod
    def __simple_str(string, max: int = 20):
        string = str(string)
        _len = len(string)
        assert max > 4, "Max length should be greater than 4."
        if _len > max:
            _half = max // 2 - 1
            return f"{string[:9]}...{string[_len - 9:]}"
        return string

    def __repr__(self):
        return f"Excel({self.__simple_str(self._path)}|{len(self)} tables)"

    def __str__(self):
        _txt = f"Excel({self.__simple_str(self._path)}|{len(self)} tables)\t" + '{\n'
        _MAX_SIZE = 16 - 2

        # Max length key
        keys = [k for k in self.keys()]
        max_len_key = max([len(key) for key in keys])
        _MAX_SIZE = min(_MAX_SIZE, max_len_key) + 2
        max_len_key = max(max_len_key, _MAX_SIZE)

        for name, tbl in self.items():
            name = self.__simple_str(name, _MAX_SIZE)
            _left_space = ' ' * (max_len_key - len(name))
            _txt += f"\t'{name}'{_left_space}: {tbl.__repr__()},\n"
        _txt += '}'
        return _txt

    def detail(self) -> str:
        _txt = f"Excel({self.__simple_str(self._path)}|{len(self)} tables)\t" + '{\n'
        _MAX_SIZE = 16 - 2

        for name, tbl in self.items():
            _sub_txt = color_string(f"\tTable '{name}'") + " >\n" + reinsert_indent(str(tbl), '\t\t')
            _txt += _sub_txt + '\n\n'

        if len(self) > 0:
            _txt = _txt[:-1]
        _txt += '}'

        return _txt

    def save(self, fpath: str = None, *, style: bool = True):
        """
        *Save the Excel object to an excel file.
        :param fpath:
        *
        :param style: bool. If True, will save the style of the cell. Default is True.
            NOTE: if use, will slower 20X and more
        :return:
        """
        wb = Workbook()
        for name, tbl in self.items():
            ws = wb.create_sheet(name)
            for row in tbl:
                _row = []
                for value in row:
                    # if nan, set to None
                    if isnan(value):
                        _row.append(None)
                    else:
                        _row.append(value)
                ws.append(_row)

            # Merge
            for merge in tbl.merges:
                ws.merge_cells(f"{merge[0].letter}:{merge[1].letter}")

            # Style
            if style and tbl.styles is not None:
                style_tbl = tbl.styles
                for i, row in enumerate(ws.iter_rows()):
                    for j, cell in enumerate(row):
                        style_tbl[i][j].apply(ws, cell)

        # remove the default sheet
        wb.remove(wb.active)

        if not fpath:
            fpath = self._path
        if not fpath:
            raise ExcelFileIOException("\n\nNo file path defined: " + str(self))

        try:
            wb.save(fpath)
        except Exception as e:
            raise ExcelFileIOException("\n\nFatal to save excel file: \n" + reinsert_indent(str(e), '\t'))
        wb.close()


if __name__ == '__main__':
    # test_listkeys_dict()
    # exit()
    # lk = ListkeysDict({'a': "Hello, ", 'b': "World"})
    # print(lk['a'])
    # print(lk)
    # lk.append('你好!')
    # print(lk)
    # lk.insert(0, 'awa')
    # print(lk)
    # del lk[:2]
    # print(lk)
    #
    # exit()
    from ffre import FileFinder

    fdir = r"C:\Users\22290\Desktop\20240504整理\tpltable 数据"
    ff = FileFinder(fdir)
    fpaths = list(ff.find(".xlsx"))

    if not fpaths:
        print("No excel file found.")
        exit(0)

    fp = fpaths[1]
    _t = TimeRecorder()
    for i in range(1):
        excel = Excel(fp, style=False)
    print("Load excel without style cost:", _t.dms(1), "ms")
    _t.tick()
    for i in range(1):
        excel = Excel(fp, style=True)
    print("Load excel with style cost:", _t.dms(1), "ms")

    excel[0].styles['A1'][TYPE_COL_WIDTH] = 200

    print(excel)
    _t.tick()
    excel.save("test.xlsx", style=False)
    print("Save excel without style cost:", _t.dms(1), "ms")
    _t.tick()
    excel.save("test_style.xlsx", style=True)
    print("Save excel with style cost:", _t.dms(1), "ms")
