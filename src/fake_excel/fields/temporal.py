from datetime import date, datetime, timezone

from faker import Faker

from fake_excel.constraint import FieldConstraint, TemporalConstraint
from fake_excel.fields.base import ExcelFieldFaker

fake = Faker()


class DateFieldFaker(ExcelFieldFaker, faker_types="date"):
    constraints: TemporalConstraint

    def get_value(self) -> str:
        return self.random_date().strftime("%Y-%m-%d")

    def random_date(self) -> date:
        start_date = self.constraints.start_date or date(1970, 1, 1)
        end_date = self.constraints.end_date or datetime.now(timezone.utc).date()
        return fake.date_time_between(start_date, end_date)

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        if not isinstance(constraints, dict):
            return TemporalConstraint()
        return TemporalConstraint(
            start_date=constraints.get("start_date"),
            end_date=constraints.get("end_date"),
            format_string=constraints.get("format_string", "%Y-%m-%d"),
        )


class TimeFieldFaker(ExcelFieldFaker, faker_types="time"):
    def get_value(self) -> str:
        return fake.time()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class DateTimeFieldFaker(ExcelFieldFaker, faker_types=["datetime", "timestamp"]):
    constraints: TemporalConstraint

    def get_value(self) -> str:
        return self.random_datetime().strftime(self.constraints.format_string)

    def random_datetime(self) -> datetime:
        epoch = datetime(1970, 1, 1, 0, 0, 0, 0, timezone.utc)
        start_value = self.constraints.start_date or epoch
        end_value = self.constraints.end_date or datetime.now(timezone.utc)
        return fake.date_time_between(start_value, end_value)

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        if not isinstance(constraints, dict):
            return TemporalConstraint(format_string="%Y-%m-%d %H:%M:%S")
        return TemporalConstraint(
            start_date=constraints.get("start_date"),
            end_date=constraints.get("end_date"),
            format_string=constraints.get("format_string", "%Y-%m-%d %H:%M:%S"),
        )
