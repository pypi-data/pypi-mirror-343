from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, Self, TypeVar, override

from polars import DataFrame, Expr
from polars.dataframe.group_by import GroupBy
from polars.datatypes import N_INFER_DEFAULT

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Sequence

    from numpy import ndarray
    from polars._typing import (
        FrameInitTypes,  # pyright: ignore[reportPrivateImportUsage]
        IntoExpr,  # pyright: ignore[reportPrivateImportUsage]
        IntoExprColumn,  # pyright: ignore[reportPrivateImportUsage]
        JoinStrategy,  # pyright: ignore[reportPrivateImportUsage]
        JoinValidation,  # pyright: ignore[reportPrivateImportUsage]
        MaintainOrderJoin,  # pyright: ignore[reportPrivateImportUsage]
        Orientation,  # pyright: ignore[reportPrivateImportUsage]
        SchemaDefinition,  # pyright: ignore[reportPrivateImportUsage]
        SchemaDict,  # pyright: ignore[reportPrivateImportUsage]
    )


_T = TypeVar("_T")
_TDataFrameWithMetaData = TypeVar(
    "_TDataFrameWithMetaData", bound="DataFrameWithMetaData"
)


class DataFrameWithMetaData(DataFrame, Generic[_T]):
    @override
    def __init__(
        self,
        data: FrameInitTypes | None = None,
        schema: SchemaDefinition | None = None,
        *,
        schema_overrides: SchemaDict | None = None,
        strict: bool = True,
        orient: Orientation | None = None,
        infer_schema_length: int | None = N_INFER_DEFAULT,
        nan_to_null: bool = False,
        metadata: _T,
    ) -> None:
        super().__init__(
            data,
            schema,
            schema_overrides=schema_overrides,
            strict=strict,
            orient=orient,
            infer_schema_length=infer_schema_length,
            nan_to_null=nan_to_null,
        )
        self.metadata = metadata

    @override
    def explode(
        self, columns: str | Expr | Sequence[str | Expr], *more_columns: str | Expr
    ) -> Self:
        return type(self)(
            data=super().explode(columns, *more_columns), metadata=self.metadata
        )

    @override
    def filter(
        self,
        *predicates: (
            IntoExprColumn
            | Iterable[IntoExprColumn]
            | bool
            | list[bool]
            | ndarray[Any, Any]
        ),
        **constraints: Any,
    ) -> Self:
        return type(self)(
            data=super().filter(*predicates, **constraints), metadata=self.metadata
        )

    @override
    def group_by(
        self,
        *by: IntoExpr | Iterable[IntoExpr],
        maintain_order: bool = False,
        **named_by: IntoExpr,
    ) -> GroupByWithMetaData[Self, _T]:
        group_by = super().group_by(*by, maintain_order=maintain_order, **named_by)
        return GroupByWithMetaData(
            group_by.df,
            *group_by.by,
            maintain_order=group_by.maintain_order,
            _cls=type(self),
            _metadata=self.metadata,
            **group_by.named_by,
        )

    @override
    def join(
        self,
        other: DataFrame,
        on: str | Expr | Sequence[str | Expr] | None = None,
        how: JoinStrategy = "inner",
        *,
        left_on: str | Expr | Sequence[str | Expr] | None = None,
        right_on: str | Expr | Sequence[str | Expr] | None = None,
        suffix: str = "_right",
        validate: JoinValidation = "m:m",
        nulls_equal: bool = False,
        coalesce: bool | None = None,
        maintain_order: MaintainOrderJoin | None = None,
    ) -> Self:
        return type(self)(
            data=super().join(
                other,
                on,
                how,
                left_on=left_on,
                right_on=right_on,
                suffix=suffix,
                validate=validate,
                nulls_equal=nulls_equal,
                coalesce=coalesce,
                maintain_order=maintain_order,
            ),
            metadata=self.metadata,
        )

    @override
    def rename(
        self, mapping: dict[str, str] | Callable[[str], str], *, strict: bool = True
    ) -> Self:
        return type(self)(
            data=super().rename(mapping, strict=strict), metadata=self.metadata
        )

    @override
    def select(
        self, *exprs: IntoExpr | Iterable[IntoExpr], **named_exprs: IntoExpr
    ) -> Self:
        return type(self)(
            data=super().select(*exprs, **named_exprs), metadata=self.metadata
        )

    @override
    def with_columns(
        self, *exprs: IntoExpr | Iterable[IntoExpr], **named_exprs: IntoExpr
    ) -> Self:
        return type(self)(
            data=super().with_columns(*exprs, **named_exprs), metadata=self.metadata
        )

    @override
    def with_row_index(self, name: str = "index", offset: int = 0) -> Self:
        return type(self)(
            data=super().with_row_index(name, offset), metadata=self.metadata
        )


class GroupByWithMetaData(GroupBy, Generic[_TDataFrameWithMetaData, _T]):
    @override
    def __init__(
        self,
        df: DataFrame,
        *by: IntoExpr | Iterable[IntoExpr],
        maintain_order: bool,
        _cls: type[_TDataFrameWithMetaData],
        _metadata: _T,
        **named_by: IntoExpr,
    ) -> None:
        super().__init__(df, *by, maintain_order=maintain_order, **named_by)
        self.cls = _cls
        self.metadata = _metadata

    @override
    def agg(
        self, *aggs: IntoExpr | Iterable[IntoExpr], **named_aggs: IntoExpr
    ) -> _TDataFrameWithMetaData:
        return self.cls(data=super().agg(*aggs, **named_aggs), metadata=self.metadata)


__all__ = ["DataFrameWithMetaData"]
