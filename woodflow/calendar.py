"""Calendar helpers for WoodFlow.

Responsible for generating working dates according to a 4-day cycle
where states 0 and 1 are working days and 2 and 3 are non-working.
"""
from datetime import datetime, timedelta
from typing import List, Tuple

_MONTHS_RU = {
    1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель",
    5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
    9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
}


def russian_month_name(month: int) -> str:
    return _MONTHS_RU.get(month, str(month))


def generate_working_dates(year: int, month: int, start_shift_counter: int) -> Tuple[List[datetime], int]:
    """Generate list of datetimes for which shift_counter < 2 in given month.

    Returns (dates, end_shift_counter) where end_shift_counter is the
    shift counter value after processing the last day of the month.
    """
    if not (1 <= month <= 12):
        raise ValueError("month must be 1..12")

    first = datetime(year, month, 1)
    if month == 12:
        after = datetime(year + 1, 1, 1)
    else:
        after = datetime(year, month + 1, 1)

    current = first
    shift = start_shift_counter % 4
    dates = []

    while current < after:
        if shift < 2:
            dates.append(current)
        # advance day and shift
        current = current + timedelta(days=1)
        shift = (shift + 1) % 4

    return dates, shift
