import datetime as dt
from collections.abc import Callable

import pytest

from liblaf import conf


@pytest.mark.parametrize(
    ("factory", "value", "expected"),
    [
        (conf.field_date, "2024-01-02", dt.date(2024, 1, 2)),
        (
            conf.field_datetime,
            "2024-01-02T03:04:05",
            dt.datetime(2024, 1, 2, 3, 4, 5, tzinfo=dt.UTC),
        ),
        (conf.field_time, "03:04:05", dt.time(3, 4, 5, tzinfo=dt.UTC)),
        (conf.field_timedelta, "PT1H30M", dt.timedelta(hours=1, minutes=30)),
    ],
)
def test_temporal_field[T](
    factory: Callable[[], conf.Field[T]], value: str, expected: T
) -> None:
    field: conf.Field[T] = factory()
    assert field.converter(value) == expected
