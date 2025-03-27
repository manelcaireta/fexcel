from faker import Faker

from fexcel.fields.base import FexcelField

fake = Faker()


class TextFieldFaker(FexcelField, faker_types=["text", "string"]):
    def get_value(self) -> str:
        return fake.text().replace("\n", " ")


class NameFieldFaker(FexcelField, faker_types="name"):
    def get_value(self) -> str:
        return fake.name()


class EmailFieldFaker(FexcelField, faker_types="email"):
    def get_value(self) -> str:
        return fake.email()


class PhoneFieldFaker(FexcelField, faker_types="phone"):
    def get_value(self) -> str:
        return fake.phone_number()


class AddressFieldFaker(FexcelField, faker_types="address"):
    def get_value(self) -> str:
        return fake.address().replace("\n", " ")


class UUIDFieldFaker(FexcelField, faker_types="uuid"):
    def get_value(self) -> str:
        return fake.uuid4()


class LocationFieldFaker(FexcelField, faker_types="location"):
    def get_value(self) -> str:
        return fake.locale()
