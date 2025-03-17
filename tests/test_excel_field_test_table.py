from dataclasses import dataclass

from fake_excel.fields import (
    AddressFieldFaker,
    BooleanFieldFaker,
    DateFieldFaker,
    DateTimeFieldFaker,
    EmailFieldFaker,
    ExcelFieldFaker,
    FloatFieldFaker,
    IntegerFieldFaker,
    IPv4FieldFaker,
    IPv6FieldFaker,
    LocationFieldFaker,
    NameFieldFaker,
    PhoneFieldFaker,
    TextFieldFaker,
    TimeFieldFaker,
    URLFieldFaker,
    UUIDFieldFaker,
)


@dataclass
class Input:
    name: str
    type: str


@dataclass
class Output:
    type: type[ExcelFieldFaker]
    pattern: str


@dataclass
class TestCase:
    input: Input
    output: Output


test_cases = [
    TestCase(
        input=Input(name="name", type="NAME"),
        output=Output(type=NameFieldFaker, pattern=r"^[a-zA-Z \.]{2,}$"),
    ),
    TestCase(
        input=Input(name="email", type="EMAIL"),
        output=Output(
            type=EmailFieldFaker,
            pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        ),
    ),
    TestCase(
        input=Input(name="phone", type="PHONE"),
        output=Output(type=PhoneFieldFaker, pattern=r"^.*$"),
    ),
    TestCase(
        input=Input(name="address", type="ADDRESS"),
        output=Output(type=AddressFieldFaker, pattern=r"^.*$"),
    ),
    TestCase(
        input=Input(name="date", type="DATE"),
        output=Output(type=DateFieldFaker, pattern=r"^\d{4}-\d{2}-\d{2}$"),
    ),
    TestCase(
        input=Input(name="time", type="TIME"),
        output=Output(type=TimeFieldFaker, pattern=r"^\d{2}:\d{2}:\d{2}$"),
    ),
    TestCase(
        input=Input(name="datetime", type="DATETIME"),
        output=Output(
            type=DateTimeFieldFaker,
            pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d*)?$",
        ),
    ),
    TestCase(
        input=Input(name="integer", type="INTEGER"),
        output=Output(type=IntegerFieldFaker, pattern=r"^-?\d+$"),
    ),
    TestCase(
        input=Input(name="float", type="FLOAT"),
        output=Output(
            type=FloatFieldFaker,
            pattern=r"^[-+]?[0-9]*(\.[0-9]*)?(e[+-]\d*)?$",
        ),
    ),
    TestCase(
        input=Input(name="boolean", type="BOOLEAN"),
        output=Output(type=BooleanFieldFaker, pattern=r"^(True|False)$"),
    ),
    TestCase(
        input=Input(name="text", type="TEXT"),
        output=Output(type=TextFieldFaker, pattern=r"^.*$"),
    ),
    TestCase(
        input=Input(name="url", type="URL"),
        output=Output(type=URLFieldFaker, pattern=r"^https?:\/\/.*[\.].*$"),
    ),
    TestCase(
        input=Input(name="ipv4", type="IPV4"),
        output=Output(
            type=IPv4FieldFaker,
            pattern=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
        ),
    ),
    TestCase(
        input=Input(name="ipv6", type="IPV6"),
        output=Output(type=IPv6FieldFaker, pattern=r"^[0-9a-fA-F:]+$"),
    ),
    TestCase(
        input=Input(name="uuid", type="UUID"),
        output=Output(
            type=UUIDFieldFaker,
            pattern=r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        ),
    ),
    TestCase(
        input=Input(name="location", type="LOCATION"),
        output=Output(type=LocationFieldFaker, pattern=r"^[a-z]{2,}_[A-Z]{2,}$"),
    ),
]
