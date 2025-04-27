from __future__ import annotations

from hypothesis import given
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
    def test_explode(self, *, df: DataFrameWithBool) -> None:
        result = df.group_by("x").agg(col("x").alias("xs")).explode("xs")
        assert isinstance(result, DataFrameWithBool)
        assert result.metadata is df.metadata

    @given(df=dataframes_with_bool())
    def test_filter(self, *, df: DataFrameWithBool) -> None:
        result = df.filter()
        assert isinstance(result, DataFrameWithBool)
        assert result.metadata is df.metadata

    @given(df1=dataframes_with_bool(), df2=dataframes_with_bool())
    def test_join(self, *, df1: DataFrameWithBool, df2: DataFrameWithBool) -> None:
        result = df1.join(df2, on=["x"])
        assert isinstance(result, DataFrameWithBool)
        assert result.metadata is df1.metadata

    @given(df=dataframes_with_bool())
    def test_rename(self, *, df: DataFrameWithBool) -> None:
        result = df.rename({"x": "x"})
        assert isinstance(result, DataFrameWithBool)
        assert result.metadata is df.metadata

    @given(df=dataframes_with_bool())
    def test_select(self, *, df: DataFrameWithBool) -> None:
        result = df.select()
        assert isinstance(result, DataFrameWithBool)
        assert result.metadata is df.metadata

    @given(df=dataframes_with_bool())
    def test_with_columns(self, *, df: DataFrameWithBool) -> None:
        result = df.with_columns()
        assert isinstance(result, DataFrameWithBool)
        assert result.metadata is df.metadata

    @given(df=dataframes_with_bool())
    def test_with_row_index(self, *, df: DataFrameWithBool) -> None:
        result = df.with_row_index()
        assert isinstance(result, DataFrameWithBool)
        assert result.metadata is df.metadata
