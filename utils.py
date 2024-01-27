from typing import Type


def type_as_string(data_type: Type) -> str:
    return data_type.__name__
