import pytest
from woodflow import calendar
from datetime import datetime


def test_feb_leap_year():
    # Feb 2024 is leap year -> 29 days
    dates, end = calendar.generate_working_dates(2024, 2, 0)
    # ensure dates are all in February
    assert all(d.month == 2 and d.year == 2024 for d in dates)
    # ensure end shift is (start + 29) % 4
    assert end == (0 + 29) % 4


def test_month_crossing_pattern():
    start = 1
    jan_dates, end_jan = calendar.generate_working_dates(2025, 1, start)
    feb_dates, end_feb = calendar.generate_working_dates(2025, 2, end_jan)

    # The shift after jan should match start + 31 mod 4
    assert end_jan == (start + 31) % 4
    assert all(d.month == 2 for d in feb_dates)
