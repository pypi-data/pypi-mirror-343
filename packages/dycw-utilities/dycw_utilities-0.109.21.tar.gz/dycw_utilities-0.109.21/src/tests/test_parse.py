from __future__ import annotations

import datetime as dt
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from types import NoneType
from typing import Literal

from hypothesis import given
from hypothesis.strategies import booleans, dates, floats, integers, sampled_from, times
from pytest import raises

from tests.test_operator import TruthEnum
from tests.test_typing_funcs.with_future import (
    DataClassFutureInt,
    DataClassFutureIntEven,
    DataClassFutureIntEvenOrOddTypeUnion,
    DataClassFutureIntEvenOrOddUnion,
    DataClassFutureIntOdd,
    TrueOrFalseFutureLit,
    TrueOrFalseFutureTypeLit,
)
from utilities.errors import ImpossibleCaseError
from utilities.functions import ensure_path
from utilities.hypothesis import (
    datetime_durations,
    local_datetimes,
    numbers,
    paths,
    text_ascii,
    timedeltas_2w,
    versions,
    zoned_datetimes,
)
from utilities.math import is_equal
from utilities.parse import (
    _ParseTextExtraNonUniqueError,
    _ParseTextParseError,
    parse_text,
)
from utilities.sentinel import Sentinel, sentinel
from utilities.types import Duration, Number
from utilities.version import Version
from utilities.whenever import (
    serialize_date,
    serialize_datetime,
    serialize_duration,
    serialize_time,
    serialize_timedelta,
)


class TestParseText:
    @given(value=booleans())
    def test_bool(self, *, value: bool) -> None:
        text = str(value)
        result = parse_text(bool, text)
        assert result is value

    @given(date=dates())
    def test_date(self, *, date: dt.date) -> None:
        text = serialize_date(date)
        result = parse_text(dt.date, text)
        assert result == date

    @given(datetime=local_datetimes() | zoned_datetimes())
    def test_datetime(self, *, datetime: dt.datetime) -> None:
        text = serialize_datetime(datetime)
        result = parse_text(dt.datetime, text)
        assert result == datetime

    @given(duration=datetime_durations(two_way=True))
    def test_duration(self, *, duration: Duration) -> None:
        text = serialize_duration(duration)
        result = parse_text(Duration, text)
        assert result == duration

    @given(truth=sampled_from(TruthEnum))
    def test_enum(self, *, truth: TruthEnum) -> None:
        text = truth.name
        result = parse_text(TruthEnum, text)
        assert result is truth

    @given(value=integers())
    def test_extra_type(self, *, value: int) -> None:
        text = str(value)
        result = parse_text(
            DataClassFutureInt,
            text,
            extra={DataClassFutureInt: lambda text: DataClassFutureInt(int_=int(text))},
        )
        expected = DataClassFutureInt(int_=value)
        assert result == expected

    @given(value=floats())
    def test_float(self, *, value: float) -> None:
        text = str(value)
        result = parse_text(float, text)
        assert is_equal(result, value)

    @given(value=integers())
    def test_int(self, *, value: int) -> None:
        text = str(value)
        result = parse_text(int, text)
        assert result == value

    @given(truth=sampled_from(["true", "false"]))
    def test_literal(self, *, truth: Literal["true", "false"]) -> None:
        result = parse_text(TrueOrFalseFutureLit, truth)
        assert result == truth

    def test_none(self) -> None:
        text = str(None)
        result = parse_text(None, text)
        assert result is None

    def test_none_type(self) -> None:
        text = str(None)
        result = parse_text(NoneType, text)
        assert result is None

    @given(number=numbers())
    def test_number(self, *, number: Number) -> None:
        text = str(number)
        result = parse_text(Number, text)
        assert result == number

    @given(path=paths())
    def test_path(self, *, path: Path) -> None:
        text = str(path)
        result = parse_text(Path, text)
        assert result == path

    @given(path=paths())
    def test_path_expanded(self, *, path: Path) -> None:
        path_use = Path("~", path)
        text = str(path_use)
        result = ensure_path(parse_text(Path, text))
        assert result == result.expanduser()

    def test_nullable_number_none(self) -> None:
        text = str(None)
        result = parse_text(Number | None, text)
        assert result is None

    @given(number=numbers())
    def test_nullable_number_number(self, *, number: Number) -> None:
        text = str(number)
        result = parse_text(Number | None, text)
        assert result == number

    def test_nullable_duration_none(self) -> None:
        text = str(None)
        result = parse_text(Duration | None, text)
        assert result is None

    @given(duration=datetime_durations(two_way=True))
    def test_nullable_duration_duration(self, *, duration: Duration) -> None:
        text = serialize_duration(duration)
        result = parse_text(Duration | None, text)
        assert result == duration

    def test_nullable_int_none(self) -> None:
        text = str(None)
        result = parse_text(int | None, text)
        assert result is None

    @given(value=integers())
    def test_nullable_int_int(self, *, value: int) -> None:
        text = str(value)
        result = parse_text(int | None, text)
        assert result == value

    def test_sentinel(self) -> None:
        text = str(sentinel)
        result = parse_text(Sentinel, text)
        assert result is sentinel

    @given(text=text_ascii())
    def test_str(self, *, text: str) -> None:
        result = parse_text(str, text)
        assert result == text

    @given(time=times())
    def test_time(self, *, time: dt.time) -> None:
        text = serialize_time(time)
        result = parse_text(dt.time, text)
        assert result == time

    @given(timedelta=timedeltas_2w())
    def test_timedelta(self, *, timedelta: dt.timedelta) -> None:
        text = serialize_timedelta(timedelta)
        result = parse_text(dt.timedelta, text)
        assert result == timedelta

    @given(x=integers(), y=integers())
    def test_tuple(self, *, x: int, y: int) -> None:
        text = f"({x}, {y})"
        result = parse_text(tuple[int, int], text)
        assert result == (x, y)

    @given(truth=sampled_from(["true", "false"]))
    def test_type_literal(self, *, truth: Literal["true", "false"]) -> None:
        result = parse_text(TrueOrFalseFutureTypeLit, truth)
        assert result == truth

    @given(value=integers())
    def test_type_union_with_extra(self, *, value: int) -> None:
        def parse_even_or_odd(text: str, /) -> DataClassFutureIntEvenOrOddTypeUnion:
            value = int(text)
            match value % 2:
                case 0:
                    return DataClassFutureIntEven(even_int=value)
                case 1:
                    return DataClassFutureIntOdd(odd_int=value)
                case _:
                    raise ImpossibleCaseError(case=[f"{value=}"])

        text = str(value)
        result = parse_text(
            DataClassFutureIntEvenOrOddTypeUnion,
            text,
            extra={DataClassFutureIntEvenOrOddTypeUnion: parse_even_or_odd},
        )
        match value % 2:
            case 0:
                expected = DataClassFutureIntEven(even_int=value)
            case 1:
                expected = DataClassFutureIntOdd(odd_int=value)
            case _:
                raise ImpossibleCaseError(case=[f"{value=}"])
        assert result == expected

    @given(value=integers())
    def test_union_with_extra(self, *, value: int) -> None:
        def parse_even_or_odd(text: str, /) -> DataClassFutureIntEvenOrOddUnion:
            value = int(text)
            match value % 2:
                case 0:
                    return DataClassFutureIntEven(even_int=value)
                case 1:
                    return DataClassFutureIntOdd(odd_int=value)
                case _:
                    raise ImpossibleCaseError(case=[f"{value=}"])

        text = str(value)
        result = parse_text(
            DataClassFutureIntEvenOrOddUnion,
            text,
            extra={DataClassFutureIntEvenOrOddUnion: parse_even_or_odd},
        )
        match value % 2:
            case 0:
                expected = DataClassFutureIntEven(even_int=value)
            case 1:
                expected = DataClassFutureIntOdd(odd_int=value)
            case _:
                raise ImpossibleCaseError(case=[f"{value=}"])
        assert result == expected

    @given(version=versions())
    def test_version(self, *, version: Version) -> None:
        text = str(version)
        result = parse_text(Version, text)
        assert result == version

    def test_error_bool(self) -> None:
        with raises(
            _ParseTextParseError, match="Unable to parse <class 'bool'>; got 'invalid'"
        ):
            _ = parse_text(bool, "invalid")

    def test_error_date(self) -> None:
        with raises(
            _ParseTextParseError,
            match=r"Unable to parse <class 'datetime\.date'>; got 'invalid'",
        ):
            _ = parse_text(dt.date, "invalid")

    def test_error_datetime(self) -> None:
        with raises(
            _ParseTextParseError,
            match=r"Unable to parse <class 'datetime\.datetime'>; got 'invalid'",
        ):
            _ = parse_text(dt.datetime, "invalid")

    def test_error_duration(self) -> None:
        with raises(
            _ParseTextParseError, match=r"Unable to parse Duration; got 'invalid'"
        ):
            _ = parse_text(Duration, "invalid")

    def test_error_enum(self) -> None:
        with raises(
            _ParseTextParseError,
            match="Unable to parse <enum 'TruthEnum'>; got 'invalid'",
        ):
            _ = parse_text(TruthEnum, "invalid")

    def test_error_extra_empty(self) -> None:
        with raises(
            _ParseTextParseError,
            match="Unable to parse <class 'tests.test_typing_funcs.with_future.DataClassFutureInt'>; got 'invalid'",
        ):
            _ = parse_text(DataClassFutureInt, "invalid", extra={})

    @given(value=integers())
    def test_error_extra_non_unique(self, *, value: int) -> None:
        @dataclass(kw_only=True)
        class Parent1:
            x: int = 0

        @dataclass(kw_only=True)
        class Parent2:
            y: int = 0

        @dataclass(kw_only=True)
        class Child(Parent1, Parent2): ...

        with raises(
            _ParseTextExtraNonUniqueError,
            match="Unable to parse <class '.*'> since `extra` must contain exactly one parent class; got <function .*>, <function .*> and perhaps more",
        ):
            _ = parse_text(
                Child,
                str(value),
                extra={
                    Parent1: lambda text: Child(x=int(text)),
                    Parent2: lambda text: Child(y=int(text)),
                },
            )

    def test_error_union_type_extra(self) -> None:
        with raises(
            _ParseTextParseError,
            match=r"Unable to parse tests\.test_typing_funcs\.with_future\.DataClassFutureIntEven \| tests\.test_typing_funcs\.with_future\.DataClassFutureIntOdd; got 'invalid'",
        ):
            _ = parse_text(DataClassFutureIntEvenOrOddUnion, "invalid", extra={})

    def test_error_float(self) -> None:
        with raises(
            _ParseTextParseError, match="Unable to parse <class 'float'>; got 'invalid'"
        ):
            _ = parse_text(float, "invalid")

    def test_error_int(self) -> None:
        with raises(
            _ParseTextParseError, match="Unable to parse <class 'int'>; got 'invalid'"
        ):
            _ = parse_text(int, "invalid")

    def test_error_none(self) -> None:
        with raises(_ParseTextParseError, match="Unable to parse None; got 'invalid'"):
            _ = parse_text(None, "invalid")

    def test_error_none_type(self) -> None:
        with raises(
            _ParseTextParseError,
            match="Unable to parse <class 'NoneType'>; got 'invalid'",
        ):
            _ = parse_text(NoneType, "invalid")

    def test_error_nullable_int(self) -> None:
        with raises(
            _ParseTextParseError, match=r"Unable to parse int \| None; got 'invalid'"
        ):
            _ = parse_text(int | None, "invalid")

    def test_error_nullable_not_type(self) -> None:
        with raises(
            _ParseTextParseError,
            match=r"Unable to parse collections\.abc\.Iterable\[None\] \| None; got 'invalid'",
        ):
            _ = parse_text(Iterable[None] | None, "invalid")

    def test_error_number(self) -> None:
        with raises(
            _ParseTextParseError, match=r"Unable to parse Number; got 'invalid'"
        ):
            _ = parse_text(Number, "invalid")

    def test_error_sentinel(self) -> None:
        with raises(
            _ParseTextParseError,
            match=r"Unable to parse <class 'utilities\.sentinel\.Sentinel'>; got 'invalid'",
        ):
            _ = parse_text(Sentinel, "invalid")

    def test_error_time(self) -> None:
        with raises(
            _ParseTextParseError,
            match=r"Unable to parse <class 'datetime\.time'>; got 'invalid'",
        ):
            _ = parse_text(dt.time, "invalid")

    def test_error_timedelta(self) -> None:
        with raises(
            _ParseTextParseError,
            match=r"Unable to parse <class 'datetime\.timedelta'>; got 'invalid'",
        ):
            _ = parse_text(dt.timedelta, "invalid")

    def test_error_tuple_invalid_text(self) -> None:
        with raises(
            _ParseTextParseError,
            match=r"Unable to parse tuple\[int, int\]; got 'invalid'",
        ):
            _ = parse_text(tuple[int, int], "invalid")

    def test_error_tuple_inconsistent_args_and_texts(self) -> None:
        with raises(
            _ParseTextParseError,
            match=r"Unable to parse tuple\[int, int\]; got '\(text1, text2, text3\)'",
        ):
            _ = parse_text(tuple[int, int], "(text1, text2, text3)")

    def test_error_unknown_annotation(self) -> None:
        with raises(
            _ParseTextParseError, match=r"Unable to parse int \| str; got 'invalid'"
        ):
            _ = parse_text(int | str, "invalid")

    def test_error_unknown_type(self) -> None:
        with raises(
            _ParseTextParseError,
            match=r"Unable to parse <class 'tests\.test_typing_funcs\.with_future\.DataClassFutureInt'>; got 'invalid'",
        ):
            _ = parse_text(DataClassFutureInt, "invalid")

    def test_error_unknown_union_type(self) -> None:
        with raises(
            _ParseTextParseError,
            match=r"Unable to parse tests\.test_typing_funcs\.with_future\.DataClassFutureIntEven \| tests\.test_typing_funcs\.with_future\.DataClassFutureIntOdd; got 'invalid'",
        ):
            _ = parse_text(DataClassFutureIntEvenOrOddUnion, "invalid")

    def test_error_version(self) -> None:
        with raises(
            _ParseTextParseError,
            match=r"Unable to parse <class 'utilities\.version\.Version'>; got 'invalid'",
        ):
            _ = parse_text(Version, "invalid")
