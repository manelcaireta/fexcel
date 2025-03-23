from abc import ABC, abstractmethod


class FexcelField(ABC):
    _fakers: dict[str, type["FexcelField"]] = {}  # noqa: RUF012

    def __init__(
        self,
        field_name: str,
        **_kwargs: str | float | list,
    ) -> None:
        self.name = field_name

    def __init_subclass__(cls, *, faker_types: str | list[str]) -> None:
        cls.register_subclass(faker_types, cls)
        return super().__init_subclass__()

    @classmethod
    def register_subclass(
        cls,
        faker_types: str | list[str],
        faker_subclass: type["FexcelField"],
    ) -> None:
        if isinstance(faker_types, str):
            faker_types = [faker_types]
        for faker_type in faker_types:
            _faker_type = faker_type.lower()
            if (
                _faker_type in cls._fakers
                and faker_subclass != cls._fakers[_faker_type]
            ):
                msg = f"Field type {_faker_type} already registered"
                raise ValueError(msg)
            cls._fakers[_faker_type.lower()] = faker_subclass

    @classmethod
    def get_faker(cls, faker_type: str) -> type["FexcelField"]:
        faker_type = faker_type.lower()
        if faker_type not in cls._fakers:
            msg = f"Unknown field type: {faker_type}"
            raise ValueError(msg)
        return cls._fakers[faker_type]

    @abstractmethod
    def get_value(self) -> str: ...

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, self.__class__):
            return False
        return self.name == value.name

    def __str__(self) -> str:
        ret = f"{self.__class__.__name__} "
        ret += "{"
        ret += " ".join(
            f"{k}={v}" for k, v in self.__dict__.items() if not k.startswith("_")
        )
        ret += "}"
        return ret

    @classmethod
    def parse_field(
        cls,
        field_name: str,
        field_type: str,
        **kwargs: str | float | list,
    ) -> "FexcelField":
        faker_cls = cls.get_faker(field_type)
        return faker_cls(field_name, **kwargs)
