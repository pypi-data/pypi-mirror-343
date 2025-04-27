from __future__ import annotations

from typing import TYPE_CHECKING, Generic, Self, TypeVar, override

from polars import DataFrame
from polars.datatypes import N_INFER_DEFAULT

if TYPE_CHECKING:
    from collections.abc import Iterable

    from polars._typing import (
        FrameInitTypes,
        IntoExpr,
        Orientation,
        SchemaDefinition,
        SchemaDict,
    )


_T = TypeVar("_T")


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
    def with_columns(
        self, *exprs: IntoExpr | Iterable[IntoExpr], **named_exprs: IntoExpr
    ) -> Self:
        return type(self)(
            super().with_columns(*exprs, **named_exprs), metadata=self.metadata
        )


__all__ = ["DataFrameWithMetaData"]
