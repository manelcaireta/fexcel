class FieldConstraint:
    def __init__(self, allowed_values: list | None = None) -> None:
        self.allowed_values = allowed_values


class NumericConstraint(FieldConstraint):
    def __init__(
        self,
        min_value: float | None = None,
        max_value: float | None = None,
        allowed_values: list[float] | None = None,
    ) -> None:
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(allowed_values)
