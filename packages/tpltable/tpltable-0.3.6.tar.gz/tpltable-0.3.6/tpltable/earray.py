import re
import warnings

import numpy as np
import pandas as pd
from tpltable.core import *
from tpltable.style import Style, TYPE_BORDER

_PAT_COORD = re.compile(r"([A-Z]+)(\d+)")


class EMPTY_INDEX:
    pass


class _ExcelIndexsLike_1DArray_Def:

    def _reindexself(self) -> None:
        """
        Reindex the Series
        * Return None. Modify self._sr inplace.
        :return:
        """
        raise NotImplementedError

    def _reconstruct(self, other) -> None:
        """
        Reconstruct self
        * Return None. Modify self._sr inplace.
        :param other: inst of __class__. The other instance.
        :return:
        """
        raise NotImplementedError

    def _construct_new_from_index(self, new_index: Union[int, slice], *, inplace=False) -> '__class__() | None':
        """
        Construct a new __class__ from the new index
        * Use this instead of directly create a new __class__ object. So you can override this method to add some other logic.
        :param new_index: int|slice. The new index you want to index self
        *
        :param inplace: bool. If True, modify self inplace. If True, Return None.
        :return: inst of __class__ | None
        """
        raise NotImplementedError

    def _construct_new_from_insert(self, insert_index: int, *values, inplace=False) -> '__class__() | None':
        """
        Construct a new __class__ from the new index
        * Use this instead of directly create a new __class__ object. So you can override this method to add some other logic.
        :param insert_index: int. The index to insert before.
        :param *values: Any. The values to insert.
        :param inplace:
        :return: inst of __class__ | None
        """
        raise NotImplementedError

    def _construct_new_from_delete(self, delete_index: Union[int, slice], *, inplace=False) -> '__class__() | None':
        """
        Construct a new __class__ from the new index
        * Use this instead of directly create a new __class__ object. So you can override this method to add some other logic.
        :param delete_index: int|slice. The index to delete.
        *
        :param inplace: bool. If True, modify self inplace. If True, Return None.
        :return: inst of __class__ | None
        """
        raise NotImplementedError

    def on_subinstance(self, construction: object) -> '__class__()':
        """
        Hook function called when a subinstance is created.
        * Return the new instance. So you can modify the new instance.
        * When this method is called, self is not modified.
        :param construction: inst of __class__. The subinstance created.
        :return: inst of __class__ | None
        """
        return construction

    def on_insert(self, construction: object) -> '__class__()':
        """
        Hook function called when a subinstance is created.
        * Return the new instance. So you can modify the new instance.
        * When this method is called, self is not modified.
        :param construction: inst of __class__. The subinstance created.
        :return: inst of __class__
        """
        return construction

    def on_delete(self, construction: object) -> '__class__()':
        """
        Hook function called when a subinstance is created.
        * Return the new instance. So you can modify the new instance.
        * When this method is called, self is not modified.
        :param construction: inst of __class__. The subinstance created.
        :return: inst of __class__
        """
        return construction


class _ExcelIndexsLike_1DArray_Base(_ExcelIndexsLike_1DArray_Def):
    _CLS_DEFAULT_INDEX_TYPE = None  # "i" or "s" or None

    # None: integer index, start with 0 and label'0'
    # "i": integer index, start with 0 and label:'1'
    # "s": letter index, start with 0 and label:'A'
    def __init__(self, _from=None, *, copy: bool = True):
        self._sr: pd.Series = None

        if isinstance(_from, list):
            try:
                _from = np.array(_from)
            except Exception as e:
                raise ValueError(f"Failed to convert list to 1D array. {e}")

        if _from is None:
            self._sr = pd.Series()
        elif isinstance(_from, np.ndarray):
            # check shape
            s = _from.shape
            if np.ndim(_from) != 1:
                raise ValueError(f"Only 1D array is supported. But got {np.ndim(_from)}D array.(shape={s})")
            self._sr = pd.Series(_from)
        elif isinstance(_from, pd.Series):
            self._sr = _from
            if copy:
                self._sr = self._sr.copy()
        elif isinstance(_from, _ExcelIndexsLike_1DArray_Base):
            self._sr = _from._sr.copy()
        else:
            raise ValueError(f"Unsupported type: {type(_from)}")

        self._reindexself()

    def _reindexself(self):
        """
        Reindex the Series
        * Return None. Modify self._sr inplace.
        :return:
        """
        if self._CLS_DEFAULT_INDEX_TYPE == "s":
            self._sr.index = [get_column_letter(i + 1) for i in range(self.size)]
        elif self._CLS_DEFAULT_INDEX_TYPE == "i":
            self._sr.index = [i + 1 for i in range(self.size)]

    def _reconstruct(self, other):
        """
        Reconstruct self
        * Return None. Modify self._sr inplace.
        :param other: inst of __class__. The other instance.
        :return:
        """
        self._sr = other._sr.copy()
        self._reindexself()

    def _construct_new_from_index(self, new_index: Union[int, slice], *, inplace=False) -> '__class__() | None':
        """
        Construct a new __class__ from the new index
        * Use this instead of directly create a new __class__ object. So you can override this method to add some other logic.
        :param new_index: int|slice. The new index you want to index self
        *
        :param inplace: bool. If True, modify self inplace. If True, Return None.
        :return: inst of __class__ | None
        """
        _new = self.__class__(self._sr.iloc[new_index], copy=False)
        _new = self.on_subinstance(_new)
        if inplace:
            self._reconstruct(_new)
        else:
            return _new

    def _construct_new_from_insert(self, insert_index: int, *values, inplace=False) -> '__class__() | None':
        """
        Construct a new __class__ from the new index
        * Use this instead of directly create a new __class__ object. So you can override this method to add some other logic.
        :param insert_index: int. The index to insert before.
        :param *values: Any. The values to insert.
        :param inplace:
        :return: inst of __class__ | None
        """
        _construct = self._sr.to_list()
        values = list(values)
        _construct = _construct[:insert_index] + values + _construct[insert_index:]
        _new = self.__class__(_construct, copy=False)
        _new = self.on_insert(_new)
        if inplace:
            self._reconstruct(_new)
        else:
            return _new

    def _construct_new_from_delete(self, delete_index: Union[int, slice], *, inplace=False) -> '__class__() | None':
        """
        Construct a new __class__ from the new index
        * Use this instead of directly create a new __class__ object. So you can override this method to add some other logic.
        :param delete_index: int|slice. The index to delete. Special case: slice(None) means clear all.
        *
        :param inplace: bool. If True, modify self inplace. If True, Return None.
        :return: inst of __class__ | None
        """
        if delete_index == slice(None):
            _new = self.__class__()
        else:
            _new = self.__class__(self._sr.drop(self._sr.index[delete_index]), copy=False)
        _new = self.on_delete(_new)

        if inplace:
            self._reconstruct(_new)
        else:
            return _new

    def _parse_slice(self, key: slice) -> Tuple[int, int, int]:
        """
        Parse the slice to get the start, stop and step
        :param key: slice. The slice to parse.
        :return: start, stop, step
        """
        _start = key.start if key.start is not None else 0
        _stop = key.stop if key.stop is not None else self.size
        _step = key.step if key.step is not None else 1
        return _start, _stop, _step

    def __str__(self):
        txt = str(self._sr)

        txt = reinsert_indent(txt, indent="\t.")

        # Keep "dtype: object" not with indent
        _last_t = txt.rfind("\t")
        if _last_t > 0:
            txt = txt[:_last_t] + txt[_last_t + 2:]

        return txt

    def __len__(self):
        return self.size

    @property
    def size(self):
        return self._sr.shape[0]

    @property
    def shape(self):
        return self._sr.shape

    @property
    def ishape(self):
        return self._sr.shape[0] - 1

    def __dim1_parse_str_index(self, skey: str) -> Tuple[str, U[int, slice]]:
        """

        :param key:
        :return: type, real_index
            * type:
                ' ': 简单索引类型
                'n': 全选类型
                "s": 文本ABC索引类型
                "i": 文本123索引类型
                "t??": slice类型, ? 可以是 ' nis'中的一个
        """
        skey = skey.upper()
        # NOTE: index_from_string will thorw warning if the type is not matched
        # 先考虑是否是slice
        if ':' in skey:
            l0, l1 = split_range_from_string(skey)

            # Get type (at here, type only can be 'i' or 's')
            _t0 = 'i' if l0.isdigit() else 's'
            _t1 = 'i' if l1.isdigit() else 's'

            start, end = index_from_string(l0, should=self._CLS_DEFAULT_INDEX_TYPE, only_int=True), index_from_string(l1, should=self._CLS_DEFAULT_INDEX_TYPE, only_int=True)
            return f"t{_t0}{_t1}", slice(start, end + 1) if start <= end else slice(end, start + 1)  # NOTE: 'A:C' with 'C:A' is the same

        if _PAT_COORD.match(skey):
            raise ValueError(f"Unexpected index: {skey}.")
        _type = 'i' if skey.isdigit() else 's'
        return _type, index_from_string(skey, should=self._CLS_DEFAULT_INDEX_TYPE, only_int=True) - 1

    def _dim1_parse_index_key(self, key, *, err_when_slice=False) -> Tuple[U[str, None], U[int, slice]]:
        """
        Parse the key to get the type and index
        :param key:
        :param err_when_slice: bool. If True, raise error when slice is found.
        :return:  type, index
            * type:
                ' ': 简单索引类型
                'n': 全选类型
                "s": 文本ABC索引类型
                "i": 文本123索引类型
                "t??": slice类型, ? 可以是 ' nis'中的一个
        """
        if key is None or key is ...:
            return 'n', None
        elif isinstance(key, int):
            # NOTE:如果传入的是int，那么就是索引
            return ' ', key
        elif isinstance(key, str):
            # NOTE:交给专用于处理字符串索引的函数处理
            return self.__dim1_parse_str_index(key)
        elif isinstance(key, slice):
            if err_when_slice:
                raise ValueError(f"Unexpected slice index: {key}. (Because param err_when_slice=True).")
            _a, _b, _step = key.start, key.stop, key.step
            _atype, _aindex, _btype, _bindex = 'n', None, 'n', None
            if _a is None and _b is None:
                return "tnn", key
            if _a is not None:
                _atype, _aindex = self._dim1_parse_index_key(_a)
            if _b is not None:
                _btype, _bindex = self._dim1_parse_index_key(_b)
            if _atype != _btype:
                raise ValueError(f"Unexpected index: '{key}'. Which is not in the same type.")

            return f"t{_atype}{_btype}", slice(_aindex, _bindex, _step)
        else:
            raise ValueError(f"Unsupported type: {type(key)}")

    def __getitem__(self, key):
        _stype, _index = self._dim1_parse_index_key(key)
        if _stype == 'n':
            return self.copy()  # None or ... Type
        elif _stype[0] != 't':  # return single value directly
            return self._sr.iloc[_index]
        else:
            return self._construct_new_from_index(_index)  # slice Type

    def __setitem__(self, key, value):
        _stype, _index = self._dim1_parse_index_key(key)
        if _stype == 'n':
            _index = slice(None)
        self._sr.iloc[_index] = value  # NOTE: Set value won't change the shape. So no need to construct new one.

    def __delitem__(self, key):
        _stype, _index = self._dim1_parse_index_key(key)
        if _stype == 'n':
            self.clear()
        else:
            self._construct_new_from_delete(_index, inplace=True)


class _ExcelIndexsLike_1DArray(_ExcelIndexsLike_1DArray_Base):

    def append(self, *values):
        """
        Append values to the end of the Series
        :param values: Any. The values to append.
        :return: None
        """
        self._construct_new_from_insert(self.size, *values, inplace=True)

    def insert(self, index: Union[str, int], *values):
        """
        Insert values before the index
        :param index: int|str. The index to insert before. (Can be a column-letter string) But not support slice.
        :param values: Any. The values to insert.
        :return: None
        """
        _stype, _index = self._dim1_parse_index_key(index)
        if _stype[0] == "t" or _stype == "n":
            raise ValueError(f"Here only accept non-slice index In {self.__class__.__name__}. But got {index}")

        self._construct_new_from_insert(_index, *values, inplace=True)

    def pop(self, index: Union[str, int], n: int = 1):
        """
        Remove and return the value at the index
        :param index: int|str. The index to remove. (Can be a column-letter string) But not support slice.
        :param n: int. The number of values to remove.
            - if index + n > size, remove until the end.
        :return: Any. The removed value. (If n > 1, return a list of values)
        """
        _stype, _index = self._dim1_parse_index_key(index)
        if _stype[0] == "t" or _stype == "n":
            raise ValueError(f"Here only accept non-slice index In {self.__class__.__name__}. But got {index}")

        end = _index + n
        if end > self.size:
            end = self.size

        _poped = self._sr.iloc[_index:end].to_list()
        self._construct_new_from_delete(slice(_index, end), inplace=True)
        if n == 1:
            return _poped[0]
        return _poped

    def extend(self, other):
        """
        Extend the Series with other Series
        :param other: Series/List/NumpyArray/ExcelIndexed-1D
        :return: None
        """
        self._construct_new_from_insert(self.size, *other, inplace=True)

    def index(self, value):
        """
        Return the index of the first occurrence of value.
        :param value: Any. The value to search.
        :return: int. The index of the first occurrence of value.
        """
        _i_index = self._sr[self._sr == value].index[0]
        if self._CLS_DEFAULT_INDEX_TYPE == "s":
            return get_column_letter(_i_index + 1)
        return _i_index

    def count(self, value):
        """
        Return the number of occurrences of value.
        :param value: Any. The value to count.
        :return: int. The number of occurrences of value.
        """
        return self._sr[self._sr == value].shape[0]

    def remove(self, value):
        """
        Remove the first occurrence of value.
        :param value: Any. The value to remove.
        :return: None
        """
        _i_index = self.index(value)
        self.pop(_i_index)

    def reverse(self):
        """
        Reverse the Series in place.
        :return: None
        """
        self._construct_new_from_index(slice(None, None, -1), inplace=True)

    def clear(self):
        """
        Clear the Series.
        :return: None
        """
        self._construct_new_from_delete(slice(None), inplace=True)

    def copy(self):
        """
        Return a shallow copy of the Series.
        :return: Series. A shallow copy of the Series.
        """
        return self.__class__(self._sr.copy(), copy=False)  # NOTE: copy won't change the shape. So no need to construct new one.

    def sort(self, key=None, reverse=False):
        """
        Sort the Series in place.
        :param key: None|callable. The function to use for sorting.
        :param reverse: bool. If True, sort in descending order.
        :return: None
        """
        _construct_list = self._sr.to_list()
        _construct_list.sort(key=key, reverse=reverse)
        self._sr = pd.Series(_construct_list)  # NOTE: sort won't change the shape. So no need to construct new one.
        self._reindexself()

    def __iter__(self):
        return iter(self._sr)

    def __contains__(self, value):
        return value in self._sr

    def __eq__(self, other):
        if not isinstance(other, _ExcelIndexsLike_1DArray):
            other = self.__class__(other)
        return self._sr.equals(other._sr)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return self.extend(other)

    def __mul__(self, times: int):
        assert isinstance(times, int), "times must be an integer."
        _construct_list = []
        _sr_list = self._sr.to_list()
        for _ in range(times):
            _construct_list.extend(_sr_list)
        return self.__class__(_construct_list)


class _ROW_TYPE:
    _CLS_DEFAULT_INDEX_TYPE = "s"

    def __str__(self):
        return "Row:\n" + super().__str__() + "\n"

class _COL_TYPE:
    _CLS_DEFAULT_INDEX_TYPE = "i"

    def __str__(self):
        return "Colomn:\n" + super().__str__() + "\n"



class StyleArray(_ExcelIndexsLike_1DArray):
    def set(self, key, value):
        """
        Set the style of each cell
        :param key:
        :param value:
        :return: None
        """
        for ic in range(self.shape[0]):
            self._sr.iloc[ic][key] = value


class StyleRow(_ROW_TYPE, StyleArray):
    def __str__(self):
        return "StyleRow:\n" + StyleArray.__str__(self) + "\n"

class StyleCol(_COL_TYPE, StyleArray):
    def __str__(self):
        return "StyleCol:\n" + StyleArray.__str__(self) + "\n"


class EArray(_ExcelIndexsLike_1DArray):
    ...


class Row(_ROW_TYPE, EArray):  # Like A: (1 2 3 4)
    pass


class Col(_COL_TYPE, EArray):  # Like 1: (A B C D)
    pass


if __name__ == '__main__':
    r = Row([1, 2, 3, 4])
    print(isinstance(r, _ROW_TYPE))


