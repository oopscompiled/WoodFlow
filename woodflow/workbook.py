"""Workbook utilities for creating reports from a template."""
from typing import Iterable
import openpyxl
from datetime import datetime


def _format_date(dt: datetime) -> str:
    return dt.strftime("%d.%m.%Y")


def create_report_from_template(template_path: str, dates: Iterable[datetime]):
    """Load `template_path`, copy or rename sheets for each date and
    set cell G3 to the report header. Returns an openpyxl Workbook.
    """
    wb = openpyxl.load_workbook(template_path)
    template_ws = wb.active

    first = True
    for dt in dates:
        date_str = _format_date(dt)
        if first:
            ws = template_ws
            ws.title = date_str
            first = False
        else:
            ws = wb.copy_worksheet(template_ws)
            ws.title = date_str
        try:
            ws['G3'] = f"Отчёт: {date_str}"
        except Exception:
            # best-effort: ignore if cell cannot be written
            pass

    return wb
