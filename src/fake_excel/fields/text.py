from faker import Faker

from fake_excel.fields.base import ExcelFieldFaker

fake = Faker()


class TextFieldFaker(ExcelFieldFaker, faker_types=["text", "string"]):
    def get_value(self) -> str:
        return fake.text()


class NameFieldFaker(ExcelFieldFaker, faker_types="name"):
    def get_value(self) -> str:
        return fake.name()


class EmailFieldFaker(ExcelFieldFaker, faker_types="email"):
    def get_value(self) -> str:
        return fake.email()


class PhoneFieldFaker(ExcelFieldFaker, faker_types="phone"):
    def get_value(self) -> str:
        return fake.phone_number()


class AddressFieldFaker(ExcelFieldFaker, faker_types="address"):
    def get_value(self) -> str:
        return fake.address()


class UUIDFieldFaker(ExcelFieldFaker, faker_types="uuid"):
    def get_value(self) -> str:
        return fake.uuid4()


class LocationFieldFaker(ExcelFieldFaker, faker_types="location"):
    def get_value(self) -> str:
        return fake.locale()
