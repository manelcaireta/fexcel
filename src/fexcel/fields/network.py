from faker import Faker

from fexcel.fields.base import FexcelField

fake = Faker()


class URLFieldFaker(FexcelField, faker_types="url"):
    def get_value(self) -> str:
        return fake.url()


class IPv4FieldFaker(FexcelField, faker_types="ipv4"):
    def get_value(self) -> str:
        return fake.ipv4()


class IPv6FieldFaker(FexcelField, faker_types="ipv6"):
    def get_value(self) -> str:
        return fake.ipv6()
