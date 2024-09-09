import re


class DateValidator:
    def __init__(self):
        pass

    @classmethod
    def is_valid_date_dd_mm_yyyy(cls, date_str: str) -> bool:
        match = re.match(r"^(0?[1-9]|[1-2][0-9]|3[0-1])([-/.:])(0?[1-9]|1[0-2])\2(\d{2,4})$", date_str)
        if not match:
            return False
        day, _, month, year = match.groups()
        day, month, year = map(int, [day, month, year])
        return cls._is_valid_day_month_year(day, month, year)

    @classmethod
    def is_valid_date_mm_dd_yyyy(cls, date_str: str) -> bool:
        match = re.match(r"^(0?[1-9]|1[0-2])([-/.:])(0?[1-9]|[1-2][0-9]|3[0-1])\2(\d{2,4})$", date_str)
        if not match:
            return False
        month, _, day, year = match.groups()
        month, day, year = map(int, [month, day, year])
        return cls._is_valid_day_month_year(day, month, year)

    @classmethod
    def _is_valid_day_month_year(cls, day: int, month: int, year: int) -> bool:
        if month in [1, 3, 5, 7, 8, 10, 12]:
            max_day = 31
        elif month in [4, 6, 9, 11]:
            max_day = 30
        elif month == 2:
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                max_day = 29
            else:
                max_day = 28
        else:
            return False
        return 1 <= day <= max_day


class DateCheck:
    @staticmethod
    def is_date(date_str: str) -> bool:
        # Check if the entire string is a date
        return (
                DateValidator.is_valid_date_mm_dd_yyyy(date_str.strip()) or
                DateValidator.is_valid_date_dd_mm_yyyy(date_str.strip())
        )
