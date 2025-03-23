from abc import ABC, abstractmethod


class FexcelField(ABC):
    """
    Abstract base class representing a field in the Fexcel schema.
    Provides methods for registering and retrieving specific field types.

    This class auto-registers all its subclasses in automatically to be potentially
    selected through its `parse_field` method.

    To create a new `FexcelFaker` that generates fruit names, you would implement
    `FexcelFaker` in the following manner to later call it normally as a new field type

    >>> from fexcel import FexcelField, Fexcel
    >>>
    >>> class FruitFieldFaker(FexcelField, faker_types="fruit"):
    ...     def get_value(self) -> str:
    ...         # implement logic here
    ...         return "TEST"
    >>>
    >>> fexcel = Fexcel([{"name": "fruity", "type": "fruit"}])
    >>> fruity_field = fexcel.fields[0]
    >>> fruity_field.__class__.__name__
    'FruitFieldFaker'
    >>> fruity_field.get_value()
    'TEST'
    """

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
        """
        Register a subclass for a given faker type.

        :param faker_types: The faker types to register.
        :type faker_types: str | list[str]
        :param faker_subclass: The subclass to associate with the faker types.
        :type faker_subclass: type[`fexcel.FexcelField`]
        :raises ValueError: If a faker type is trying to get registered with an already
        registered faker name.
        """

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
        """
        Retrieve a registered faker class by its type.

        :param faker_type: The faker type to retrieve.
        :type faker_type: str
        :return: The corresponding faker class.
        :rtype: type[`fexcel.FexcelField`]
        :raises ValueError: If the faker type is unknown.
        """

        faker_type = faker_type.lower()
        if faker_type not in cls._fakers:
            msg = f"Unknown field type: {faker_type}"
            raise ValueError(msg)
        return cls._fakers[faker_type]

    @abstractmethod
    def get_value(self) -> str:
        """
        Abstract method to fake a value for the field this class is representing.

        Subclasses have to implement this method with a proper function that returns
        a fake record of the concrete type the column they are representing is supposed
        to be.

        :return: The value of the field.
        :rtype: str
        """
        ...

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
        """
        Factory method that parses a field from the `Fexcel` schema and returns a
        corresponding `FexcelField` implementation

        :param field_name: The name for the field the resulting `FexcelField` will
        represent.
        :type field_name: str
        :param field_type: The value used to parse the corresponding `FexcelField`,
        must correspond to a registered `FexcelField`
        :type field_type: str
        :return: A concrete `FexcelField` implementation
        :rtype: FexcelField
        :raises ValueError: If the faker type is unknown.
        """

        faker_cls = cls.get_faker(field_type)
        return faker_cls(field_name, **kwargs)
