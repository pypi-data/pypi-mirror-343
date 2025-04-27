from __future__ import annotations

from hypothesis import assume, given
from hypothesis.strategies import DrawFn, booleans, composite, lists, tuples
from polars import DataFrame, Int64, String, col
from utilities.hypothesis import int64s, text_ascii

from polars_subclasses.lib import DataFrameWithMetaData


class DataFrameWithBool(DataFrameWithMetaData[bool]): ...


@composite
def dataframes_with_bool(draw: DrawFn, /) -> DataFrameWithBool:
    rows = draw(lists(tuples(int64s(), text_ascii())))
    bool_ = draw(booleans())
    return DataFrameWithBool(
        data=rows, schema={"x": Int64, "y": String}, orient="row", metadata=bool_
    )


class TestDataFrameWithMetaData:
    @given(df=dataframes_with_bool())
    def test_main(self, *, df: DataFrameWithBool) -> None:
        assert isinstance(df, DataFrameWithBool)
        assert isinstance(df, DataFrameWithMetaData)
        assert isinstance(df, DataFrame)

    @given(df=dataframes_with_bool())
    def test_drop(self, *, df: DataFrameWithBool) -> None:
        self._assert(df.drop(), df)

    @given(df=dataframes_with_bool())
    def test_drop_nans(self, *, df: DataFrameWithBool) -> None:
        self._assert(df.drop_nans(), df)

    @given(df=dataframes_with_bool())
    def test_drop_nulls(self, *, df: DataFrameWithBool) -> None:
        self._assert(df.drop_nulls(), df)

    @given(df=dataframes_with_bool())
    def test_explode(self, *, df: DataFrameWithBool) -> None:
        self._assert(df.group_by("x").agg(col("x").alias("xs")).explode("xs"), df)

    @given(df=dataframes_with_bool())
    def test_filter(self, *, df: DataFrameWithBool) -> None:
        self._assert(df.filter(), df)

    @given(df=dataframes_with_bool())
    def test_head(self, *, df: DataFrameWithBool) -> None:
        self._assert(df.head(), df)

    @given(df1=dataframes_with_bool(), df2=dataframes_with_bool())
    def test_join(self, *, df1: DataFrameWithBool, df2: DataFrameWithBool) -> None:
        self._assert(df1.join(df2, on=["x"]), df1)

    @given(df=dataframes_with_bool())
    def test_rename(self, *, df: DataFrameWithBool) -> None:
        self._assert(df.rename({"x": "x"}), df)

    @given(df=dataframes_with_bool())
    def test_reverse(self, *, df: DataFrameWithBool) -> None:
        self._assert(df.reverse(), df)

    @given(df=dataframes_with_bool())
    def test_sample(self, *, df: DataFrameWithBool) -> None:
        _ = assume(not df.is_empty())
        self._assert(df.sample(), df)

    @given(df=dataframes_with_bool())
    def test_select(self, *, df: DataFrameWithBool) -> None:
        self._assert(df.select(), df)

    @given(df=dataframes_with_bool())
    def test_shift(self, *, df: DataFrameWithBool) -> None:
        self._assert(df.shift(), df)

    @given(df=dataframes_with_bool())
    def test_tail(self, *, df: DataFrameWithBool) -> None:
        self._assert(df.tail(), df)

    @given(df=dataframes_with_bool())
    def test_with_columns(self, *, df: DataFrameWithBool) -> None:
        self._assert(df.with_columns(), df)

    @given(df=dataframes_with_bool())
    def test_with_row_index(self, *, df: DataFrameWithBool) -> None:
        self._assert(df.with_row_index(), df)

    def _assert(self, result: DataFrameWithBool, df: DataFrameWithBool, /) -> None:
        assert isinstance(result, DataFrameWithBool)
        assert result.metadata is df.metadata
