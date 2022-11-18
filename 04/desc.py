# An integer is positive if it is greater than zero, and negative if it is less than zero.
# Zero is defined as neither negative nor positive.


class Integer:
    __val: int

    def __init__(self, val: int = 0):
        self.__val = val

    def __get__(self, obj, objtype):
        return self.__val

    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise TypeError(
                f"Can't assign {value} of type {type(value)} to an Integer's field"
            )
        self.__val = value


class String:
    __val: str

    def __init__(self, val: str = ""):
        self.__val = val

    def __get__(self, obj, objtype):
        return self.__val

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError(
                f"Can't assign {value} of type {type(value)} to String's field"
            )
        self.__val = value


class PositiveInteger:
    __val: int

    def __init__(self, val: int = 1):
        self.__val = val

    def __get__(self, obj, objtype):
        return self.__val

    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise TypeError(
                f"Can't assign {value} of type {type(value)} to PositiveInteger's field"
            )
        if value <= 0:
            raise ValueError(
                f"Can't assign non-positive value = {value} to PositiveInteger's field"
            )
        self.__val = value
