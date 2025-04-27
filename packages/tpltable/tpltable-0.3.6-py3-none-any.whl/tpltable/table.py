import pandas as pd
from tpltable.earray import *
from tpltable.earray import _ExcelIndexsLike_1DArray, _PAT_COORD, _ROW_TYPE, _COL_TYPE


class _ExcelIndexsLike_2DArray_Def:

    def _reindexself(self) -> None:
        """
        Reindex the DataFrame inplace
        * Return None. Modify self._df inplace.
        :return:
        """
        raise NotImplementedError

    def _reconstruct(self, other) -> None:
        """
        Reconstruct self
        * Return None. Modify self._df inplace.
        :param other: inst of __class__. The other instance.
        :return:
        """
        raise NotImplementedError

    def _construct_new_from_index(self, new_index0: Union[int, slice], new_index1: Union[int, slice], *, inplace=False) -> '__class__() | None':
        """
        Construct a new __class__ from the new index
        * Use this instead of directly create a new __class__ object. So you can override this method to add some other logic.
        :param new_index0: int|slice. The new index of axis=0 (Row) you want to index self
        :param new_index1: int|slice. The new index of axis=1 (Col) you want to index self
        *
        :param inplace: bool. If True, modify self inplace. If True, Return None.
        :return: inst of __class__ | None
        """
        raise NotImplementedError

    def _construct_new_from_insert(self, insert_index0: Union[int, slice], insert_index1: Union[int, slice], *values, inplace=False) -> '__class__() | None':
        """
        Construct a new __class__ from the new index
        * Use this instead of directly create a new __class__ object. So you can override this method to add some other logic.
        :param insert_index0: int|slice. The index to insert before at axis=0 (Row).
        :param insert_index1: int|slice. The index to insert before at axis=1 (Col).
            * Note:至多只能有一个维度是slice，且此时value必须是另一个维度的EArray

        :param *values: Any. The values to insert.
        :param inplace:
        :return: inst of __class__ | None
        """
        assert not (isinstance(insert_index0, slice) and isinstance(insert_index1, slice)), "At most one dimension can be slice in insert-construction."
        raise NotImplementedError

    def _construct_new_from_delete(self, delete_index0: Union[int, slice], delete_index1: Union[int, slice], *, inplace=False) -> '__class__() | None':
        """
        Construct a new __class__ from the new index
        * Use this instead of directly create a new __class__ object. So you can override this method to add some other logic.
        :param delete_index0: int|slice. The index at axis=0 (Row) to delete.
        :param delete_index1: int|slice. The index at axis=1 (Col) to delete.
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



class _ExcelIndexsLike_2DArray_Base(_ExcelIndexsLike_2DArray_Def):
    __NAN_PAT = re.compile(r"(\snan\s)|(\s<NA>\s)", re.I)
    _ROW_CLS = Row
    _COL_CLS = Col

    @staticmethod
    def __NAN_SUB_FN(match_obj):
        tar_string = match_obj.group()
        _s, _e = tar_string[0], tar_string[-1]
        return f"{_s}NaN{_e}"

    def __init__(self, _from=None, *, copy: bool = True):
        self._df: pd.DataFrame = None
        if isinstance(_from, pd.DataFrame):
            self._df = _from
            if copy:
                self._df = self._df.copy()
        elif isinstance(_from, np.ndarray):
            # check shape
            s = _from.shape
            if np.ndim(_from) != 2:
                raise ValueError(f"Only 2D array is supported. But got {np.ndim(_from)}D array.(shape={s})")
            self._df = pd.DataFrame(_from)
        elif isinstance(_from, list):
            if not _from:
                self._df = pd.DataFrame()
            else:
                try:
                    _construct_list = []
                    for i, _l in enumerate(_from):
                        if isinstance(_l, Col):
                            _construct_list.append(_l._sr.to_list())
                            warnings.warn(
                                f"Table's input should be rows, but got a column. Regarded as a row.(at index:{i})"
                            )
                        elif isinstance(_l, _ExcelIndexsLike_1DArray):
                            _construct_list.append(_l._sr.to_list())
                        elif isinstance(_l, list):
                            _construct_list.append(_l.copy())
                        elif hasattr(_l, 'tolist'):
                            _construct_list.append(_l.tolist())
                        elif hasattr(_l, 'to_list'):
                            _construct_list.append(_l.to_list())
                        else:
                            raise ValueError(f"Unsupported type in list(at index:{i}): {type(_l)}")
    
                    # 找到最长的列表长度
                    max_length = max(len(s) for s in _construct_list)
    
                    # 填充所有列表
                    for i, _l in enumerate(_construct_list):
                        _len = len(_l)
                        if _len < max_length:
                            _construct_list[i] = _l + [np.nan] * (max_length - _len)
    
                    arr = np.array(_construct_list)
    
                    # 将填充后的列表转换为DataFrame
                    self._df = pd.DataFrame(arr)
    
                    # 检查DataFrame是否为2D
                    if self._df.ndim != 2:
                        raise ValueError(f"Only 2D array is supported. But got {self._df.ndim}D array from list.(shape={self._df.shape})")
    
                except Exception as e:
                    raise ValueError(f"Failed to convert list to 2D array. {e}")
        elif isinstance(_from, _ExcelIndexsLike_2DArray):
            self._df = _from._df.copy()
        elif _from is None:
            self._df = pd.DataFrame()
        else:
            raise ValueError(f"Unsupported type: {type(_from)}")

        # set index(col with ABCD, row with 1234)
        self._reindexself()

    def _reindexself(self) -> None:
        """
        Reindex self inplace
        * Return None. Modify self._df inplace.
        """
        row_index = [i + 1 for i in range(self._df.shape[0])]
        col_index = [get_column_letter(i + 1) for i in range(self._df.shape[1])]
        self._df.index = row_index
        self._df.columns = col_index

    def _reconstruct(self, other) -> None:
        """
        Reconstruct self
        * Return None. Modify self._df inplace.
        """
        self._df = other._df.copy()
        self._reindexself()

    def _construct_new_from_index(self, new_index0: Union[int, slice], new_index1: Union[int, slice], *, inplace=False) -> '__class__() | None':
        """
        Construct a new __class__ from the new index
        * Use this instead of directly create a new __class__ object. So you can override this method to add some other logic.
        :param new_index0: int|slice. The new index of axis=0 (Row) you want to index self
        :param new_index1: int|slice. The new index of axis=1 (Col) you want to index self
        *
        :param inplace: bool. If True, modify self inplace. If True, Return None.
        :return: inst of __class__ | None
        """
        _new = self.__class__(self._df.loc[new_index0, new_index1], copy=False)
        if inplace:
            self._reconstruct(_new)
            return
        return _new

    def _construct_new_from_insert(self, insert_index0: Union[int, slice], insert_index1: Union[int, slice], *values, inplace=False) -> '__class__() | None':
        """
        Construct a new __class__ from the new index
        * Use this instead of directly create a new __class__ object. So you can override this method to add some other logic.
        :param insert_index0: int|slice. The index to insert before at axis=0 (Row).
        :param insert_index1: int|slice. The index to insert before at axis=1 (Col).
            * Note:有且只能有一个维度是slice，且此时value必须是另一个维度的EArray

        :param *values: Row|Col. The values to insert.
        :param inplace:
        :return: inst of __class__ | None
        """
        _construct_list = self._df.values.tolist()
        if isinstance(insert_index0, slice):
            if isinstance(insert_index1, slice):
                raise ValueError("At most one dimension can be slice in insert-construction.")
            values = [self._COL_CLS(v) for v in values]
            for i, _l in enumerate(_construct_list):
                _this_row_inserted = [v[i] for v in values]  # get the row at cols
                _construct_list[i] = _l[:insert_index1] + _this_row_inserted + _l[insert_index1:]
        elif isinstance(insert_index1, slice):
            values = [self._ROW_CLS(v) for v in values]
            _these_rows_inserted = [list(v) for v in values]
            _construct_list = _construct_list[:insert_index0] + _these_rows_inserted + _construct_list[insert_index0:]
        else:
            raise ValueError("At least one dimension should be slice in insert-construction.")

        _new = self.__class__(_construct_list, copy=False)
        if inplace:
            self._reconstruct(_new)
            return
        return _new

    def _construct_new_from_delete(self, delete_index0: Union[int, slice], delete_index1: Union[int, slice], *, inplace=False) -> '__class__() | None':
        """
        Construct a new __class__ from the new index
        * Use this instead of directly create a new __class__ object. So you can override this method to add some other logic.
        :param delete_index0: int|slice. The index at axis=0 (Row) to delete.
        :param delete_index1: int|slice. The index at axis=1 (Col) to delete.
        *
        :param inplace: bool. If True, modify self inplace. If True, Return None.
        :return: inst of __class__ | None
        """
        if delete_index0 == slice(None) or delete_index1 == slice(None):
            _new = self.__class__(None, copy=False)
        else:
            if isinstance(delete_index0, slice):
                if isinstance(delete_index1, slice):
                    _new = self.__class__(self)
                    # set to nan
                    _new._df.loc[delete_index0, delete_index1] = pd.NA
                else:
                    _new = self.__class__(self._df.drop(delete_index0, axis=0), copy=False)
            elif isinstance(delete_index1, slice):
                _new = self.__class__(self._df.drop(delete_index1, axis=1), copy=False)
            else:
                _new = self.__class__(self)
                _new._df.iloc[delete_index0, delete_index1] = pd.NA

        if inplace:
            self._reconstruct(_new)
            return
        return _new


    def __str__(self):
        _values = self._df.values.tolist()
        _values2 = []

        # make sure each one is string
        for i, _l in enumerate(_values):
            _values[i] = [str(v) if not isnan(v) else "NaN" for v in _l]
            _values2.append([f"({v})" if not isnan(v) else "NaN" for v in _l])

        _cnd = np.array(_values)
        _bracket_cdf = np.array(_values2)

        # 将处于merge范围内的元素加上(), 除了第一个元素
        _unhandled_mask = np.ones(self._df.shape, dtype=bool)
        for lt, rb in self._merges:
            _new_mask = np.zeros(self._df.shape, dtype=bool)
            _new_mask[lt.ir:rb.ir + 1, lt.ic:rb.ic + 1] = _unhandled_mask[lt.ir:rb.ir + 1, lt.ic:rb.ic + 1]
            _cnd[_new_mask] = _bracket_cdf[_new_mask]
            # 把第一个元素还原
            if _unhandled_mask[lt.ir, lt.ic]:
                _cnd[lt.ir, lt.ic] = ':' + _cnd[lt.ir, lt.ic][1:]
            _unhandled_mask[lt.ir:rb.ir + 1, lt.ic:rb.ic + 1] = False

        return str(pd.DataFrame(_cnd, index=self._df.index, columns=self._df.columns, copy=False))

    def __repr__(self):
        c = Coord(self._df.shape[1] - 1, self._df.shape[0] - 1)
        return f"Table[:'{c.letter}']"

    @property
    def size(self):

        return self._df.shape

    @property
    def shape(self):
        return self._df.shape

    @property
    def ishape(self):
        _r, _c = self._df.shape
        return _r - 1, _c - 1

    def __dim2_parse_1dim_str_index(self, skey: str) -> Tuple[str, U[int, slice]]:
        """

        :param key:
        :return: type, real_index
            * type:
                ' ': 简单索引类型
                "s": 文本ABC索引类型
                "i": 文本123索引类型
                "t??": slice类型, ? 可以是 ' nis'中的一个
        """
        # NOTE: index_from_string will thorw warning if the type is not matched
        # 先考虑是否是slice
        if ':' in skey:
            l0, l1 = split_range_from_string(skey)

            # Get type (at here, type only can be 'c'、'i' or 's')
            _t0 = 'c' if _PAT_COORD.match(l0) else ('i' if l0.isdigit() else 's')
            _t1 = 'c' if _PAT_COORD.match(l0) else ('i' if l1.isdigit() else 's')

            start, end = index_from_string(l0), index_from_string(l1)
            if _t1 == 'c':
                return f"t{_t0}{_t1}", slice(start, end)
            return f"t{_t0}{_t1}", slice(start - 1, end)

        if _PAT_COORD.match(skey):
            return "c", Coord.FromLetter(skey)

        _type = 'i' if skey.isdigit() else 's'

        return _type, index_from_string(skey, only_int=True) - 1

    def __dim2_parse_1dim_index_key(self, key) -> Tuple[U[str, None], U[int, slice]]:
        """
        Parse the key to get the type and index
        :param key:
        :return:  type, index
            * type:
                ' ': 简单索引类型
                'c': 文本Coord索引类型
                "s": 文本ABC索引类型
                "i": 文本123索引类型
                "t??": slice类型, ? 可以是 ' nisc'中的一个
        """

        if key is None or key is ...:
            return 'n', slice(None)
        elif isinstance(key, int):
            # NOTE:如果传入的是int，那么就是索引
            return ' ', key
        elif isinstance(key, str):
            # NOTE:交给专用于处理字符串索引的函数处理
            return self.__dim2_parse_1dim_str_index(key)
        elif isinstance(key, slice):
            _a, _b, _step = key.start, key.stop, key.step
            if _a is None and _b is None:
                return "tnn", key
            _atype, _aindex, _btype, _bindex, _any_flag = 'n', None, 'n', None, False
            if _a is not None:
                _atype, _aindex = self.__dim2_parse_1dim_index_key(_a)
                _any_flag = True
            if _b is not None:
                _btype, _bindex = self.__dim2_parse_1dim_index_key(_b)
                _any_flag = True
            assert _atype[0] != 't' and _btype[0] != 't', f"Unexpected slice index: {key}"
            return f"t{_atype}{_btype}", slice(_aindex, _bindex, _step)
        else:
            raise ValueError(f"Unsupported type: {type(key)}")

    def _dim2_parse_index_key(self, key) -> Tuple[U[int, slice, None, object], U[int, slice, None]]:
        """
        Parse the key to get the type and index
        :param key:
        :return:  index0, index1
            * type:
                '.': 简单索引类型  对应 'n', ' ', 't  '中的一个(可以直接被传入DataFrame)
                'c': 文本Coord索引类型
                "s": 文本ABC索引类型
                "i": 文本123索引类型
                "t??": slice类型, ? 可以是 ' nisc'中的一个
                'm': mask索引类型
        """

        if hasattr(key, 'shape') and key.shape == self.shape:
            return key, None

        _is_tuple = isinstance(key, tuple)
        # NOTE: 两个元素独立解析
        if _is_tuple:
            assert len(key) == 2, f"Only accept 2-tuple(2D). But got {len(key)}-tuple:{key}."
            _t0, _i0 = self.__dim2_parse_1dim_index_key(key[0])
            _t1, _i1 = self.__dim2_parse_1dim_index_key(key[1])
        else:
            _t0, _i0 = self.__dim2_parse_1dim_index_key(key)
            _t1, _i1 = 'n', None

        _ts, _is = [_t0, _t1], [_i0, _i1]

        # NOTE: 剪枝, 将对称的 tsc tcs tic tci化简为 tcc
        for i, (_type, _index) in enumerate(zip(_ts.copy(), _is.copy())):
            if _type[0] == 't':
                _c0, _c1, _c2 = _type
                if _c1 == 'c':
                    if _c2 == 's':  # 'A1:E' -> 'A1:E1'
                        _ts[i] = 'tcc'
                        c: Coord = _index.start.copy()
                        c.c = _index.stop
                        _is[i] = slice(_index.start, c, _index.step)
                    elif _c2 == 'i':  # 'A1:4' -> 'A1:A4'
                        _ts[i] = 'tcc'
                        c: Coord = _index.start.copy()
                        c.r = _index.stop
                        _is[i] = slice(_index.start, c, _index.step)
                elif _c2 == 'c':
                    if _c1 == 's':  # 'A:E1' -> 'A1:E1'
                        _ts[i] = 'tcc'
                        c: Coord = _index.stop.copy()
                        c.c = _index.start
                        _is[i] = slice(c, _index.stop, _index.step)
                    elif _c1 == 'i':  # '1:A4' -> 'A1:A4'
                        _ts[i] = 'tcc'
                        c: Coord = _index.stop.copy()
                        c.r = _index.start
                        _is[i] = slice(c, _index.stop, _index.step)
        _t0, _t1 = _ts
        _i0, _i1 = _is

        # NOTE: 排除禁止的情况
        # > 1. 单个元素的情况都是可行的
        # > 2. 两个元素的情况:
        '''
            . i s c tii tss tcc
            ...代表 'n', ' ', 't  '中的一个(可以直接被传入DataFrame). 称其为'.'
            t[..., ...] ok
            *t[..., '1'] t['1', ...] ok explain as a '1', ...
            t[..., 'A'] *t['A', ...] ok explain as a ..., 'A'
            t[..., 'A1'] t['A1', ...] err
            *t[..., '1:2'] t['1:2', ...] ok explain as a '1:2', ...
            t[..., 'A:B'] *t['A:B', ...] ok explain as a ..., 'A:B'
            t[..., 'A1:B2'] t['A1:B2', ...] err
            ------------------------------------------------------
            t['1', '2'] err
            t['1', 'A'] *t['A', '1'] ok explain as a '1', 'A'
            t['1', 'A4'] t['A1', '4'] ok explain as a 'A1', 'A4'
            t['1', '1:2'] t['1:2', '1'] err
            t['1', 'A:B'] *t['A:B', '1'] ok explain as a '1', 'A:B'
            t['1', 'A1:B2'] err
            ------------------------------------------------------
            t['A', 'B'] err
            t['A', 'E1'] t['A1', 'E'] ok explain as a 'A1', 'E1'
            *t['A', '1:2'] t['1:2', 'A'] ok explain as a '1:2', 'A'
            t['A', 'A:B'] t['A', 'A:B'] err
            t['A', 'A1:B2'] t['A1', 'A2'] err
            ------------------------------------------------------
            t['A1', 'B2'] ok
            t['A1', '1:2'] err
            t['A1', 'A:B'] err
            t['A1', 'A1:B2'] err
            ------------------------------------------------------
            t['1:2', '1:2'] err
            t['1:2', 'A:B'] *t['A:B', '1:2'] ok explain as a '1:2', 'A:B'
            t['1:2', 'A1:B2'] err
            ------------------------------------------------------
            t['A:B', 'A:B'] err
            t['A:B', 'A1:B2'] err
            ------------------------------------------------------
            t['A1:B2', 'A3:C3'] err
        '''
        if _t0 == 'n' or _t0 == ' ' or _t0 == 't  ':
            _t0 = '.'
        if _is_tuple:
            if _t1 == 'n' or _t1 == ' ' or _t1 == 't  ':
                _t1 = '.'
            if _t0 == '.':
                # .. is ok
                # .s is ok, like (:, 'A')
                # .tss is ok, like (:, 'A:B')
                if _t1 == 'i':
                    _t0, _t1 = _t1, _t0
                    _i0, _i1 = _i1, _i0
                elif _t1 == 'c':
                    raise ValueError(f"Unexpected index: {key}.  # .|c like (:, 'A1') is err")
                elif _t1 == 'tii':
                    _i0, _i1 = _i1, _i0
                elif _t1 == 'tcc':
                    raise ValueError(f"Unexpected index: {key}.  # .|tcc like (:, 'A1:B2') is err")
            elif _t0 == 'i':
                # i. is ok, like ('1', :)
                # is is ok, like ('1', 'A')
                # itss is ok, like ('1', 'A:B')
                if _t1 == 'i':
                    raise ValueError(f"Unexpected index: {key}.  # i|i like ('1', '2') is err")
                elif _t1 == 'c':
                    c: Coord = _i1.copy()
                    c.ir = _i0
                    _t0, _i0 = 'c', c
                elif _t1 == 'tii':
                    raise ValueError(f"Unexpected index: {key}.  # i|tii like ('1', '1:2') is err")
                elif _t1 == 'tcc':
                    raise ValueError(f"Unexpected index: {key}.  # i|tcc like ('1', 'A1:B2') is err")
            elif _t0 == 's':
                if _t1 == 's':
                    raise ValueError(f"Unexpected index: {key}.  # s|s like ('A', 'B') is err")
                elif _t1 == '.':
                    _t0, _t1 = _t1, _t0
                    _i0, _i1 = _i1, _i0
                elif _t1 == 'i':
                    _t0, _t1 = _t1, _t0
                    _i0, _i1 = _i1, _i0
                elif _t1 == 'c':
                    c: Coord = _i1.copy()
                    c.ic = _i0
                    _t0, _i0 = 'c', c
                elif _t1 == 'tii':
                    _t0, _t1 = _t1, _t0
                    _i0, _i1 = _i1, _i0
                elif _t1 == 'tss':
                    raise ValueError(f"Unexpected index: {key}.  # s|tss like ('A', 'A:B') is err")
                elif _t1 == 'tcc':
                    raise ValueError(f"Unexpected index: {key}.  # s|tcc like ('A', 'A1:B2') is err")
            elif _t0 == 'c':
                # cc is ok, like ('A1', 'B2')
                if _t1 == '.':
                    raise ValueError(f"Unexpected index: {key}.  # c|. like ('A1', :) is err")
                elif _t1 == 'i':
                    c: Coord = _i0.copy()
                    c.ir = _i1
                    _t1, _i1 = 'c', c
                elif _t1 == 's':
                    c: Coord = _i0.copy()
                    c.ic = _i1
                    _t1, _i1 = 'c', c
                elif _t1 == 'tii':
                    raise ValueError(f"Unexpected index: {key}.  # c|tii like ('A1', '1:2') is err")
                elif _t1 == 'tss':
                    raise ValueError(f"Unexpected index: {key}.  # c|tss like ('A1', 'A:B') is err")
                elif _t1 == 'tcc':
                    raise ValueError(f"Unexpected index: {key}.  # c|tcc like ('A1', 'A1:B2') is err")
            elif _t0 == 'tii':
                # tii. is ok, like ('1:2', :)
                # tiis is ok, like ('1:2', 'A')
                # tiitss is ok, like ('1:2', 'A:B')
                if _t1 == 'i':
                    raise ValueError(f"Unexpected index: {key}.  # tii|i like ('1:2', '2') is err")
                elif _t1 == 'c':
                    raise ValueError(f"Unexpected index: {key}.  # tii|c like ('1:2', 'A1') is err")
                elif _t1 == 'tii':
                    raise ValueError(f"Unexpected index: {key}.  # tii|tii like ('1:2', '1:2') is err")
                elif _t1 == 'tcc':
                    raise ValueError(f"Unexpected index: {key}.  # tii|tcc like ('1:2', 'A1:B2') is err")
            elif _t0 == 'tss':
                if _t1 == '.':
                    _t0, _t1 = _t1, _t0
                    _i0, _i1 = _i1, _i0
                elif _t1 == 'i':
                    _t0, _t1 = _t1, _t0
                    _i0, _i1 = _i1, _i0
                elif _t1 == 's':
                    raise ValueError(f"Unexpected index: {key}.  # tss|s like ('A:B', 'B') is err")
                elif _t1 == 'c':
                    raise ValueError(f"Unexpected index: {key}.  # tss|c like ('A:B', 'A1') is err")
                elif _t1 == 'tii':
                    _t0, _t1 = _t1, _t0
                    _i0, _i1 = _i1, _i0
                elif _t1 == 'tss':
                    raise ValueError(f"Unexpected index: {key}.  # tss|tss like ('A:B', 'A:B') is err")
                elif _t1 == 'tcc':
                    raise ValueError(f"Unexpected index: {key}.  # tss|tcc like ('A:B', 'A1:B2') is err")
            elif _t0 == 'tcc':
                if _t1 == '.':
                    raise ValueError(f"Unexpected index: {key}.  # tcc|. like ('A1:B2', :) is err")
                elif _t1 == 'i':
                    raise ValueError(f"Unexpected index: {key}.  # tcc|i like ('A1:B2', '2') is err")
                elif _t1 == 's':
                    raise ValueError(f"Unexpected index: {key}.  # tcc|s like ('A1:B2', 'B') is err")
                elif _t1 == 'c':
                    raise ValueError(f"Unexpected index: {key}.  # tcc|c like ('A1:B2', 'A1') is err")
                elif _t1 == 'tii':
                    raise ValueError(f"Unexpected index: {key}.  # tcc|tii like ('A1:B2', '1:2') is err")
                elif _t1 == 'tss':
                    raise ValueError(f"Unexpected index: {key}.  # tcc|tss like ('A1:B2', 'A:B') is err")
                elif _t1 == 'tcc':
                    raise ValueError(f"Unexpected index: {key}.  # tcc|tcc like ('A1:B2', 'A1:B2') is err")
        elif _t0 == 's' or _t0 == 'tss':
            _t0, _t1 = '.', _t0
            _i0, _i1 = slice(None), _i0

        # NOTE: 展开包含c的情况(经过上面的处理，这里只剩下了 cc cn tccn 的情况)
        if _is_tuple and _t0 == 'c' and _t1 == 'c':
            _i0, _i1 = slice(_i0.ir, _i1.ir + 1), slice(_i0.ic, _i1.ic + 1)
        elif not _is_tuple and _t0 == 'c':
            _i0, _i1 = _i0.ir, _i0.ic
        elif not _is_tuple and _t0 == 'tcc':
            _i0, _i1 = slice(_i0.start.ir, _i0.stop.ir + 1), slice(_i0.start.ic, _i0.stop.ic + 1)
        elif not _is_tuple and _t1 != 's' and _t1 != 'tss':  # NOTE: 经过上一步骤后，t0变为.，所以t1才是原来的t0
            _i1 = None

        # NOTE: 返回
        if _t0 == '.' and isinstance(_i0, slice) and _i0.start is None and _i0.stop is None:
            _t0 = None

        return _i0, _i1



class _ExcelIndexsLike_2DArray(_ExcelIndexsLike_2DArray_Base):


    @property
    def _other_raws(self):
        return tuple()


    def _reconstruct(self, *args, **kwargs):
        new = self.__class__(*args, **kwargs)
        self._df = new._df
        return new

    def _enlarge(self, ir, ic, fill=np.nan):
        """
        Enlarge the table to include the coord,
        :param ir:
        :param ic:
        :param fill:
        :return:
        """
        sr, sc = self._df.shape
        sr, sc = sr - 1, sc - 1

        if isinstance(ir, slice):
            ir = ir.stop if ir.stop is not None else sr

        if isinstance(ic, slice):
            ic = ic.stop if ic.stop is not None else sc

        if ir is None:
            ir = sr
        if ic is None:
            ic = sc

        # if less than shape, return
        if ir <= sr and ic <= sc:
            return

        # enlarge the table
        _2d_list = self._df.values.tolist()
        if ir > sr:
            _2d_list += [[fill] * sc for _ in range(ir - sr)]
        if ic > sc:
            for _l in _2d_list:
                _l.extend([fill] * (ic - sc))
        self._reconstruct(_2d_list, *self._other_raws, copy=False)

    def __getitem__(self, key):
        """
        Get the value of the key
        :param key:
        :return: value|Row|Col|Table
        """
        _i0, _i1 = self._dim2_parse_index_key(key)
        if _i0 is None:  # None, None
            return self
        elif _i1 is None:
            if isinstance(_i0, slice):
                return self.__class__(self._df.iloc[_i0], *self._other_raws, copy=False)
            return self._ROW_CLS(self._df.iloc[_i0], copy=False)
        else:
            if isinstance(_i0, slice):
                if isinstance(_i1, slice):
                    return self.__class__(self._df.iloc[_i0, _i1], *self._other_raws, copy=False)
                return self._COL_CLS(self._df.iloc[_i0, _i1], copy=False)
            if isinstance(_i1, slice):
                return self._ROW_CLS(self._df.iloc[_i0, _i1], copy=False)
            return self._df.iloc[_i0, _i1]

    def __setitem__(self, key, value):
        """
        Set the value of the key
        :param key:
        :param value:
        :return: None
        """
        _i0, _i1 = self._dim2_parse_index_key(key)

        if _i0 is not None and _i1 is not None:
            _is_i0_slice = isinstance(_i0, slice)
            _is_i1_slice = isinstance(_i1, slice)
            if _is_i0_slice and _is_i1_slice:
                if _i0.start is None and _i0.stop is None and _i1.start is None and _i1.stop is None:
                    _i0 = _i1 = None
                elif _i0.start is None and _i0.stop is None:
                    _i0 = slice(None)
                elif _i1.start is None and _i1.stop is None:
                    _i1 = None
                else:  # 区域赋值
                    self._enlarge(_i0.stop, _i1.stop, fill=np.nan)
                    self._df.iloc[_i0, _i1] = value
            elif _is_i0_slice and _i0.start is None and _i0.stop is None:
                _i0 = slice(None)
            elif _is_i1_slice and _i1.start is None and _i1.stop is None:
                _i1 = None
            else:  # 元素赋值
                self._enlarge(_i0, _i1, fill=np.nan)
                self._df.iloc[_i0, _i1] = value

        if _i0 is None:  # None, None
            if isinstance(value, (int, float, str, bool)):
                self._df.iloc[:, :] = value  # NOTE: 使用:,:来避免修改形状
                return
            elif isinstance(value, list):
                value = np.array(value)
                if value.ndim == 1:
                    value = value.reshape(1, -1)
                elif value.ndim > 2:
                    raise ValueError(f"Only 1D or 2D array is supported. But got {_.ndim}D array.")

            if hasattr(value, 'shape'):
                if value.shape == self._df.shape:
                    self._df.iloc[:, :] = value
                else:
                    self._reconstruct(value, *self._other_raws, copy=False)
                return
            else:
                raise ValueError(f"Unsupported value type: {type(value)}")

        elif _i1 is None:
            if isinstance(value, (int, float, str, bool)):
                self._df[_i0] = value
                return
            elif isinstance(value, list):
                value = np.array(value)
                if value.ndim == 1:
                    value = value.reshape(1, -1)
                elif value.ndim > 2:
                    raise ValueError(f"Only 1D or 2D array is supported. But got {_.ndim}D array.")

            if hasattr(value, 'shape'):
                if value.shape == self._df.shape:
                    self._df.iloc[_i0, :] = value
                else:
                    _2d_list = self._df.values.tolist()
                    # del these rows
                    del _2d_list[_i0]
                    # insert new rows at the start
                    _start = _i0.start if isinstance(_i0, slice) else _i0
                    _start = 0 if _start is None else _start
                    if hasattr(value, 'tolist'):
                        _ = value.tolist()
                    elif hasattr(value, 'to_list'):
                        _ = value.to_list()
                    else:
                        raise ValueError(f"Unsupported value type: {type(value)}")
                    _2d_list = _2d_list[:_start] + _ + _2d_list[_start:]
                    self._reconstruct(_2d_list, *self._other_raws, copy=False)
                return
            else:
                raise ValueError(f"Unsupported value type: {type(value)}")
        else:
            self._df.iloc[_i0, _i1] = value

    def __delitem__(self, key):
        """
        Delete the value of the key
        :param key:
        :return: None
        """
        _i0, _i1 = self._dim2_parse_index_key(key)
        if _i0 is None:
            self._reconstruct(None, *self._other_raws)
            return
        elif _i1 is None:
            self._df.drop(self._df.index[_i0], inplace=True)
            self._reindexself()
            return
        else:
            _is_i0_slice = isinstance(_i0, slice)
            _is_i1_slice = isinstance(_i1, slice)
            if _is_i0_slice and _is_i1_slice:
                if _i0.start is None and _i0.stop is None and _i1.start is None and _i1.stop is None:
                    self._reconstruct()
                elif _i0.start is None and _i0.stop is None:
                    self._df.drop(self._df.columns[_i1], axis=1, inplace=True)
                    self._reindexself()
                elif _i1.start is None and _i1.stop is None:
                    self._df.drop(self._df.index[_i0], inplace=True)
                    self._reindexself()
                else:  # 删除一片区域为nan
                    self._df.iloc[_i0, _i1] = np.nan
            elif _is_i0_slice and _i0.start is None and _i0.stop is None:
                self._df.drop(self._df.columns[_i1], axis=1, inplace=True)
                self._reindexself()
                return
            elif _is_i1_slice and _i1.start is None and _i1.stop is None:
                self._df.drop(self._df.index[_i0], inplace=True)
                self._reindexself()
                return
            else:
                self._df.iloc[_i0, _i1] = np.nan

    def append(self, *values, axis=0):
        """
        Append Rows to the end of the table
        :param values:
        :param axis: 0: row, 1: col
        :return: None
        """
        assert 0 <= axis <= 1, f"Unsupported axis: {axis}"
        _construct = self._df.values.tolist()
        if axis == 0:
            _construct.extend(values)
        else:
            for row in _construct:
                row.extend(values)
        self._reconstruct(_construct, *self._other_raws, copy=False)

    def clear(self):
        """
        Clear the table
        :return: None
        """
        self._reconstruct(None, *self._other_raws)

    def copy(self):
        """
        Copy the table
        :return: Table
        """
        return self.__class__(self._df, *self._other_raws)

    def resize(self, perferrence, fill=NaN):
        """
        Resize the table
        :param perferrence: tuple of new size|other Table.size
        :return:
        """
        _has_fill_copy = hasattr(fill, 'copy')
        if isinstance(perferrence, tuple):
            _new_r, _new_c = perferrence
        elif hasattr(perferrence, 'shape'):
            _new_r, _new_c = perferrence.shape
        else:
            raise ValueError(f"Unsupported preferrence type: {type(perferrence)}")

        assert _new_r >= 0 and _new_c >= 0, f"Invalid size: ({_new_r}, {_new_c})"

        _r, _c = self.shape
        if _r == _new_r and _c == _new_c:
            return

        if _new_r == 0 or _new_c == 0:
            self.clear()
            return

        if _r == 0 or _c == 0:
            _construct = [[fill.copy() if _has_fill_copy else fill for _ in range(_new_c)] for _ in range(_new_r)]
            self._reconstruct(_construct, *self._other_raws, copy=False)
            return

        # 先考虑扩张
        if _r < _new_r:
            self.append(*[[fill.copy() if _has_fill_copy else fill] * _c for _ in range(_new_r - _r)], axis=0)
        if _c < _new_c:
            self.append(*[fill.copy() if _has_fill_copy else fill for _ in range(_new_c - _c)], axis=1)

        # 再考虑缩小 NOTE: 缩小不必考虑label的问题
        if _r > _new_r:
            self._reconstruct(self._df.iloc[:_new_r], *self._other_raws, copy=False)
        if _c > _new_c:
            self._reconstruct(self._df.iloc[:, :_new_c], *self._other_raws, copy=False)

    def __iter__(self):
        for _r in self._df.values.tolist():
            yield _r

    def __contains__(self, item):
        for _r in self._df.values.tolist():
            if item in _r:
                return True
        return False

    def __eq__(self, other):
        if isinstance(other, Table):
            return self._df.equals(other._df)
        return np.array(self._df) == other

    def __ne__(self, other):
        if isinstance(other, Table):
            return not self._df.equals(other._df)
        return np.array(self._df) != other

    def __len__(self):
        return self.shape[0]

class StyleTable(_ExcelIndexsLike_2DArray):
    _ROW_CLS = StyleRow
    _COL_CLS = StyleCol

    def set(self, key, value):
        """
        Set the style of each cell
        :param key:
        :param value:
        :return: None
        """
        for ir in range(self.shape[0]):
            for ic in range(self.shape[1]):
                self._df.iloc[ir, ic][key] = value


class Table(_ExcelIndexsLike_2DArray):
    # def __init__(self, _from=None, *, copy: bool = True):
    def __init__(self, data=None, styles=None, merges: list = None, *, copy: bool = True):
        super().__init__(data, copy=copy)
        self._styles = StyleTable() if styles is None else (styles.copy() if isinstance(styles, StyleTable) else StyleTable(styles))
        self._merges = []

        self.__raw_merges = merges

        self.styles.resize(self.shape, fill=Style.Default())

        if merges is not None:
            for _m in merges:
                if isinstance(_m, tuple):
                    self.merge(*_m)
                else:
                    self.merge(_m)

    @property
    def styles(self):
        return self._styles

    @property
    def merges(self):
        return self._merges

    def merge(self, key: U[int, str, slice, None], key1: U[int, str, slice, None] = EMPTY_INDEX, *, border: Border = None):
        if key1 is not EMPTY_INDEX:
            key = key, key1

        lt, rb = None, None
        _i0, _i1 = self._dim2_parse_index_key(key)
        ishape = self.ishape
        if _i0 is None:
            lt, rb = Coord(0, 0), Coord(ishape[1], ishape[0])
        elif _i1 is None:
            if isinstance(_i0, slice):
                lt, rb = Coord(_i0.start, 0), Coord(_i0.stop - 1, self.ishape[0] - 1)
            else:
                lt, rb = Coord(0, _i0), Coord(self.ishape[1] - 1, _i0 - 1)
        else:
            if isinstance(_i0, slice):
                if isinstance(_i1, slice):
                    lt, rb = Coord(_i1.start, _i0.start), Coord(_i1.stop - 1, _i0.stop - 1)
                else:
                    lt, rb = Coord(_i1, _i0.start), Coord(_i1 - 1, _i0.stop - 1)
            else:
                if isinstance(_i1, slice):
                    lt, rb = Coord(_i1.start, _i0), Coord(_i1.stop - 1, _i0 - 1)
                else:
                    lt, rb = Coord(_i1, _i0), Coord(_i1 - 1, _i0 - 1)

        # check whether the merge is out of the table
        if lt.ir > ishape[0] or lt.ic > ishape[1]:
            return

        if rb.ir > ishape[0]:
            rb.ir = ishape[0]

        if rb.ic > ishape[1]:
            rb.ic = ishape[1]

        self._merges.append((lt, rb))

        if border is not None:
            self._styles[key].set(TYPE_BORDER, border)

    # def _reconstruct(self, *args, **kwargs):
    #     """
    #     用于缩小或扩大表格时自动同步调整styles
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     new = super()._reconstruct(*args, **kwargs)
    #     self._styles = new._styles
    #     return new

    # def __delitem__(self, key):
    #     """
    #     Delete the value of the key
    #     :param key:
    #     :return: None
    #     """
    #     _i0, _i1 = self._dim2_parse_index_key(key)
    #     if _i0 is None:
    #         self._reconstruct(None, *self._other_raws, copy=False)
    #         return
    #     elif _i1 is None:
    #         self._df.drop(self._df.index[_i0], inplace=True)
    #         self._styles._df.drop(self._styles._df.index[_i0], inplace=True)
    #         self._remerge('dr', _i0)
    #         self._reindexself()
    #         return
    #     else:
    #         _is_i0_slice = isinstance(_i0, slice)
    #         _is_i1_slice = isinstance(_i1, slice)
    #         if _is_i0_slice and _is_i1_slice:
    #             if _i0.start is None and _i0.stop is None and _i1.start is None and _i1.stop is None:
    #                 self._reconstruct(None, *self._other_raws, copy=False)
    #             elif _i0.start is None and _i0.stop is None:
    #                 self._df.drop(self._df.columns[_i1], axis=1, inplace=True)
    #                 self._styles._df.drop(self._styles._df.columns[_i1], axis=1, inplace=True)
    #                 self._remerge('dc', _i1)
    #                 self._reindexself()
    #             elif _i1.start is None and _i1.stop is None:
    #                 self._df.drop(self._df.index[_i0], inplace=True)
    #                 self._styles._df.drop(self._styles._df.index[_i0], inplace=True)
    #                 self._remerge('dr', _i0)
    #                 self._reindexself()
    #             else:  # 删除一片区域为nan
    #                 self._df.iloc[_i0, _i1] = np.nan
    #         elif _is_i0_slice and _i0.start is None and _i0.stop is None:
    #             self._df.drop(self._df.columns[_i1], axis=1, inplace=True)
    #             self._styles._df.drop(self._styles._df.columns[_i1], axis=1, inplace=True)
    #             self._remerge('dc', _i1)
    #             self._reindexself()
    #             return
    #         elif _is_i1_slice and _i1.start is None and _i1.stop is None:
    #             self._df.drop(self._df.index[_i0], inplace=True)
    #             self._styles._df.drop(self._styles._df.index[_i0], inplace=True)
    #             self._remerge('dr', _i0)
    #             self._reindexself()
    #             return
    #         else:
    #             self._df.iloc[_i0, _i1] = np.nan

    def _remerge(self, op_type, value):
        """
        重新调整合并区域
        :param op_type: 'a'|'d'+'r'|'c'  表示增加行、删除行、增加列、删除列
        :param value: 对应的索引值，可以是int或slice
        :return: None
        """
        assert len(op_type) == 2, f"Invalid op_type: {op_type}"
        op, tar = op_type
        assert op in 'ad' and tar in 'rc', f"Invalid op_type: {op_type}"

        # 将int转为slice
        if isinstance(value, int):
            value = slice(value, value + 1)
        elif not isinstance(value, slice):
            raise ValueError(f"Unsupported re_merge value type: {type(value)}")
        _removes = []
        if tar == 'r':
            for i, (lt, rb) in enumerate(self._merges.copy()):
                if op == 'a':
                    if lt.ir >= value.start:
                        lt.ir += value.stop - value.start
                    if rb.ir >= value.start:
                        rb.ir += value.stop - value.start
                else:
                    if lt.ir >= value.start:
                        lt.ir -= value.stop - value.start
                    if rb.ir >= value.start:
                        rb.ir -= value.stop - value.start
                if lt.ir == rb.ir:
                    _removes.append(i)
                # else:  NOTE: 无需赋值, 只是浅拷贝
                #     self._merges[i] = (lt, rb)
        else:
            for i, (lt, rb) in enumerate(self._merges.copy()):
                if op == 'a':
                    if lt.ic >= value.start:
                        lt.ic += value.stop - value.start
                    if rb.ic >= value.start:
                        rb.ic += value.stop - value.start
                else:
                    if lt.ic >= value.start:
                        lt.ic -= value.stop - value.start
                    if rb.ic >= value.start:
                        rb.ic -= value.stop - value.start
                if lt.ic == rb.ic:
                    _removes.append(i)
                # else:  NOTE: 无需赋值, 只是浅拷贝
                #     self._merges[i] = (lt, rb)


def __1d_test(_print=True):

    d = [1, 2, 3, 4, 5]

    r = Row(d)
    c = Col(d)

    if _print: print(f"字符串化测试：\n{r}\n{c}")
    if _print: print(f"size shape 测试：\n{r.size} {r.shape}")

    if _print: print(f"索引测试：\n{r[0]} {r['2']} {r['C']} {r['3:2']}")

    r[0] = 10
    r['2'] = 20
    r['C'] = 30
    r[1:3] = [100, 200]
    if _print: print(f"赋值测试：\n{r}")

    r.append(1000)
    r.insert(2, 2000)
    if _print: print(f"添加测试：\n{r}")

    if _print: print(f"弹出测试：\n{r.pop(2)} {r} {r.pop(1, 2)} {r}")

    r.extend([1, 2, 3])
    if _print: print(f"扩展测试：\n{r}")

    del r[0]
    del r['2']
    if _print: print(f"删除测试：\n{r}")


def _1d_unit_test(_print=True):
    tc = TimeRecorder()
    __1d_test(_print)
    warnings.filterwarnings('ignore')
    for i in range(999):
        __1d_test(_print)
    warnings.filterwarnings('default')
    print(f"测试结束，耗时: {tc.dms(1000)} ms / 测试")


def __2d_test(_print=True):
    import colorama
    r0 = Col([1, 2, 3, 4, 5])
    r1 = [6, 7, 8, 9, 10]
    r2 = Row([11, 12, 13, 14, 15])
    r3 = Row([16, 17, 18, 19, 20])

    t = Table([r0, r1, r2, r3])
    print(f"赋值 t = Table:\n{t}\n")
    colors = [colorama.Fore.RED, colorama.Fore.GREEN, colorama.Fore.BLUE, colorama.Fore.YELLOW, colorama.Fore.MAGENTA]
    # 详细的get测试
    tests_0 = {
        '0': 0, '...': ..., '1:2': slice(1, 2), '"A"': 'A', '"A1"': 'A1', '"A:B"': 'A:B', '"1:2"': '1:2', '"A1:B2"': 'A1:B2',
        '0, "1"': (0, '1'), '"1", 0': ('1', 0), '0:1, "1"': (slice(0, 1), '1'), '"1", 0:1': ('1', slice(0, 1)),
        '0, "A"': (0, 'A'), '"A", 0': ('A', 0), '0:1, "A"': (slice(0, 1), 'A'), '"A", 0:1': ('A', slice(0, 1)),
        '0, "1:2"': (0, '1:2'), '"1:2", 0': ('1:2', 0), '0:1, "1:2"': (slice(0, 1), '1:2'), '"1:2", 0:1': ('1:2', slice(0, 1)),
        '0, "A:B"': (0, 'A:B'), '"A:B", 0': ('A:B', 0), '0:1, "A:B"': (slice(0, 1), 'A:B'), '"A:B", 0:1': ('A:B', slice(0, 1)),
        # --------------------------------------------------------------------------------------------
        '"1", "A"': ('1', 'A'), '"A", "1"': ('A', '1'),
        '"1", "A4"': ('1', 'A4'), '"A1", "4"': ('A1', '4'),
        '"1", "A:B"': ('1', 'A:B'), '"A:B", "1"': ('A:B', '1'),
        # --------------------------------------------------------------------------------------------
        '"A", "E1"': ('A', 'E1'), '"A1", "E"': ('A1', 'E'),
        '"A", "1:2"': ('A', '1:2'), '"1:2", "A"': ('1:2', 'A'),
        # --------------------------------------------------------------------------------------------
        '"A1", "B2"': ('A1', 'B2'),

    }
    for i, (show_key, test_key) in enumerate(tests_0.items()):
        if show_key == '"1:2"':
            ...  # debug
        color = colors[i % len(colors)]
        # print(f"Test for + c + 't[{show_key}]' + r + :\n{t[test_key]}\n")
        print(f"{color}Test for" + color + f"'t[{show_key}]'" + colorama.Fore.RESET + f":\n{t[test_key]}\n")

    t['C2'] = 114514
    print(f"赋值 t['C2'] = 114514:\n{t}\n")
    t['A1:B2'] = [[100, 200], [300, 400]]
    print(f"赋值 t['A1:B2'] = [[100, 200], [300, 400]]:\n{t}\n")
    t[0] = [5, 4, 3, 2, 1]
    print(f"赋值 t[0] = [5, 4, 3, 2, 1]:\n{t}\n")
    t[0] = [1, 2, 3, 4, 5, 6]
    print(f"赋值 t[0] = [1, 2, 3, 4, 5, 6]:\n{t}\n")
    t['F7'] = 233
    print(f"赋值 t['F7'] = 233:\n{t}\n")
    del t['C2']
    print(f"删除 t['C2']:\n{t}\n")
    del t['A1:B2']
    print(f"删除 t['A1:B2']:\n{t}\n")
    del t[0]
    print(f"删除 t[0]:\n{t}\n")
    del t['A']
    print(f"删除 t['A']:\n{t}\n")
    del t['1:2']
    print(f"删除 t['1:2']:\n{t}\n")
    del t['A:B']
    print(f"删除 t['A:B']:\n{t}\n")

    t[t == 233] = 114514
    print(f"替换 t[t==233] = 114514:\n{t}\n")


if __name__ == '__main__':
    import time

    # _a = time.time()
    # for i in range(1):
    #     __1d_test(1)
    # print(f"Finish Test. Cost:{round((time.time() - _a) * 1000, 2)} ms")
    # exit(0)

    __2d_test()
