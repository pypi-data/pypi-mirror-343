"""
Author: Big Panda
Created Time: 25.04.2025 14:38
Modified Time: 25.04.2025 14:38
Description:
    The structure of number:
        1. real number:
            {1}. Rational numbers: in computer, the rational number can be regarded same as real number
                [1]. Integers:
                    1). Whole numbers:
                        One. Natural / Counting Numbers:
                [2]. Float numbers(Fractional nuber)
           {2}: Irrational numbers:
        2. imaginary number: Complex number

    Real number: RealProperty
    Rational number: RationalProperty
    Integer: IntProperty
    Float: FloatProperty
"""
from __future__ import annotations
from DataRestriction.ErrorMessages import error_message

__all__ = ["RealProperty",
           "RationalProperty",
           "IntProperty",
           "FloatProperty",
           "StringProperty"]


class RealProperty:
    _value: int | float
    _doc: str

    def __init__(self: RealProperty, default: int | float = 1.0, doc: str = "") -> None:
        self.value: int = default
        self.doc: str = doc

    @property
    def value(self: RealProperty) -> int | float:
        return self._value

    @value.setter
    def value(self: RealProperty, new_value: int | float) -> None:
        if isinstance(new_value, (int, float)):
            self._value = new_value
        elif isinstance(new_value, bool):
            raise ValueError(error_message["is boolean"])
        else:
            raise ValueError(error_message["not real"])

    @property
    def doc(self: RealProperty) -> str:
        return self._doc

    @doc.setter
    def doc(self: RealProperty, new_doc: str) -> None:
        if not isinstance(new_doc, str):
            raise ValueError(error_message["not string"])
        self._doc = new_doc

    def __repr__(self: RealProperty) -> str:
        return str(self._value)

    def __str__(self: RealProperty) -> str:
        return str(self._value)

    def __int__(self: RealProperty) -> int:
        return int(self._value)

    def __float__(self: RealProperty) -> float:
        return float(self._value)

    def __add__(self: RealProperty, other: int | float):
        return self._value + other

    def __sub__(self: RealProperty, other: int | float):
        return self._value - other

    def __mul__(self: RealProperty, other: int | float):
        return self._value * other

    def __truediv__(self: RealProperty, other: int | float):
        return self._value / other

    def __floordiv__(self: RealProperty, other: int | float):
        return self._value // other

    def __mod__(self: RealProperty, other: int | float):
        return self._value % other

    def __eq__(self: RealProperty, other: int | float):
        return self._value == other

    def __abs__(self: RealProperty):
        return abs(self._value)

    def __pow__(self: RealProperty, other: int | float):
        return self._value ** other

    # The other methods still need to be added


class RationalProperty(RealProperty):
    ...


class IntProperty(RationalProperty):
    _value: int
    _doc: str

    def __init__(self: IntProperty, default: int = 1, doc: str = "") -> None:
        super().__init__(default=default, doc=doc)

    @property
    def value(self: IntProperty) -> int:
        return self._value

    @value.setter
    def value(self: IntProperty, new_value: int) -> None:
        if not self._is_integer(new_value):
            raise ValueError(error_message["not int"])
        self._value = new_value

    @staticmethod
    def _is_integer(value: int) -> bool:
        if isinstance(value, bool):
            raise ValueError(error_message["is boolean"])
        return isinstance(value, int)

        # For strict data type, we do not need to consider the situation below.
        # (isinstance(value, float) and value.is_integer() and not isinstance(value, bool)))


class FloatProperty(RationalProperty):
    _value: float
    _doc: str

    def __init__(self: FloatProperty, default: float = 1.0, doc: str = "") -> None:
        super().__init__(default=default, doc=doc)

    @property
    def value(self: FloatProperty) -> float:
        return self._value

    @value.setter
    def value(self: FloatProperty, new_value: float) -> None:
        if isinstance(new_value, float):
            self._value = new_value
        elif isinstance(new_value, bool):
            raise ValueError(error_message["is boolean"])
        elif isinstance(new_value, int):
            raise ValueError(error_message["is int"])
        else:
            raise ValueError(error_message["not float"])


class StringProperty:
    _value: str
    _doc: str

    def __init__(self: StringProperty, default: str = "", doc: str = "") -> None:
        self.value: str = default
        self.doc: str = doc

    @property
    def value(self: StringProperty) -> str:
        return self._value

    @value.setter
    def value(self: StringProperty, new_value: str) -> None:
        if not isinstance(new_value, str):
            raise ValueError(error_message["not str"])
        self._value = new_value

    @property
    def doc(self: StringProperty) -> str:
        return self._doc

    @doc.setter
    def doc(self: StringProperty, new_doc: str) -> None:
        if not isinstance(new_doc, str):
            raise ValueError(error_message["not string"])
        self._doc = new_doc


if __name__ == '__main__':
    # ==================================== Test RealProperty ====================================
    # num = RealProperty(default=1.0)
    # print(num)
    # ==================================== Test IntProperty ====================================
    num = IntProperty(default=1)
    print(num)
    # ==================================== Float RealProperty ====================================
    # num = FloatProperty(default=1)
    # print(num)
    ...
