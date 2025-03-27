from datetime import datetime, timezone
from typing import Any

from faker import Faker

from fexcel.fields.base import FexcelField

fake = Faker()


class DateTimeFieldFaker(FexcelField, faker_types=["datetime", "timestamp"]):
    def __init__(
        self,
        field_name: str,
        *,
        start_date: str | datetime | None = None,
        end_date: str | datetime | None = None,
        format_string: str = "%Y-%m-%d %H:%M:%S",
        **kwargs: Any,
    ) -> None:
        super().__init__(field_name, **kwargs)

        self.format_string = format_string

        if isinstance(start_date, str):
            start_date = self._ensure_datetime(start_date, "start_date")
        self.start_date = start_date

        if isinstance(end_date, str):
            end_date = self._ensure_datetime(end_date, "end_date")
        self.end_date = end_date

    def _ensure_datetime(self, value: str, var_name: str) -> datetime | None:
        try:
            self._try_parse_datetime(value)
        except ValueError as err:
            msg = (
                f"Invalid {var_name}: {value}. A Date or Datetime "
                "can only be in ISO601 or with a user provided format string"
            )
            raise ValueError(msg) from err

    def _try_parse_datetime(self, value: str) -> datetime | None:
        try:
            return datetime.strptime(value, self.format_string).astimezone(timezone.utc)
        except ValueError:
            return datetime.fromisoformat(value)

    def get_value(self) -> str:
        return self.random_datetime().strftime(self.format_string)

    def random_datetime(self) -> datetime:
        epoch = datetime(1970, 1, 1, 0, 0, 0, 0, timezone.utc)
        start_value = self.start_date or epoch
        end_value = self.end_date or datetime.now(timezone.utc)
        return fake.date_time_between(start_value, end_value)


class DateFieldFaker(DateTimeFieldFaker, faker_types="date"):
    def __init__(
        self,
        field_name: str,
        *,
        start_date: str | datetime | None = None,
        end_date: str | datetime | None = None,
        format_string: str = "%Y-%m-%d",
    ) -> None:
        super().__init__(
            field_name=field_name,
            start_date=start_date,
            end_date=end_date,
            format_string=format_string,
        )

    def get_value(self) -> str:
        return self.random_datetime().date().strftime(self.format_string)


class TimeFieldFaker(FexcelField, faker_types="time"):
    def get_value(self) -> str:
        return fake.time()
