from faker import Faker

from fexcel.fields.base import ExcelFieldFaker

fake = Faker()


class URLFieldFaker(ExcelFieldFaker, faker_types="url"):
    def get_value(self) -> str:
        return fake.url()


class IPv4FieldFaker(ExcelFieldFaker, faker_types="ipv4"):
    def get_value(self) -> str:
        return fake.ipv4()


class IPv6FieldFaker(ExcelFieldFaker, faker_types="ipv6"):
    def get_value(self) -> str:
        return fake.ipv6()
