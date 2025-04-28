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
import numpy as np

__all__ = ["RealProperty",
           "RationalProperty",
           "IntProperty",
           "FloatProperty",
           "StringProperty",
           "Point2D",
           "Coord2D"]


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


class Point2D:
    _x: int | float = 0
    _y: int | float = 0
    _doc: str

    def __init__(self: Point2D, *args) -> None:
        """
        Define two methods for initializing Point2D
            1. point = Points2D((x, y))
            2. point = Points2D([x, y])
            3. point = Points2D({'x' : x, 'y' : y})
            4. point = Points2D(x, y)
            5. point = Points2D(Points2D(x, y), (offset_x, offset_y))
            6. point = Points2D(Points2D(x, y), [offset_x, offset_y])
        """
        if len(args) == 0:
            pass
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, (tuple, list)) and len(arg) == 2:
                self.x, self.y = arg
            elif isinstance(arg, dict):
                self.x = arg.get('x', 0.0)
                self.y = arg.get('y', 0.0)
            else:
                raise ValueError(error_message["Point2D one argument"])
        elif len(args) == 2:
            if isinstance(args[0], (int, float)) and isinstance(args[1], (int, float)):
                self.x, self.y = args
            elif isinstance(args[0], Point2D) and isinstance(args[1], (tuple, list)) and len(args[1]) == 2:
                self.x, self.y = args[0].x + args[1][0], args[0].y + args[1][1]
            else:
                raise ValueError(error_message["Point2D two arguments"])
        else:
            raise ValueError(error_message["Point2D initialize"])

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(error_message["Point2D x not rational"])
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(error_message["Point2D y not rational"])
        self._y = value

    # String representation of Point2D
    def __str__(self: Point2D) -> str:
        return f"Point2D{self.x, self.y}"

    def __repr__(self: Point2D) -> str:
        return f"Point2D{self.x, self.y}"

    # Override setitem method
    def __setitem__(self: Point2D, key: int, value: int | float) -> None:
        if key == 0:
            self.x: int | float = value
        elif key == 1:
            self.y: int | float = value
        else:
            raise ValueError(error_message["Point2D index out range"])

    # Override getitem method
    def __getitem__(self: Point2D, key: int) -> float:
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise ValueError('The index of Point2D object is out of range.')

    def __iter__(self: Point2D) -> iter(Point2D):
        return iter([self.x, self.y])

    def __copy__(self: Point2D) -> Point2D:
        return Point2D(self.x, self.y)

    def __neg__(self: Point2D) -> Point2D:
        return Point2D(-self.x, -self.y)

    def __abs__(self: Point2D) -> Point2D:
        """
        Get absolute point coordinates of current one. In first Quadrant.
        """
        return Point2D(abs(self.x), abs(self.y))

    def __add__(self: Point2D, point2d: Point2D) -> Point2D:
        """
        Point2D operation ------ Adding
        """
        return Point2D(self.x + point2d.x, self.y + point2d.y)

    def __sub__(self: Point2D, point2d: Point2D) -> Point2D:
        """
        Point2D operation ------ Subtraction
        """
        return Point2D(self.x - point2d.x, self.y - point2d.y)

    # ================================================= Specific function =================================================
    def tolist(self):
        return [self.x, self.y]

    def index(self: Point2D, num: int | float) -> int:
        """
        Return the index of coordinate equals to num
        :param num: reference number
        :return: 0 for x, 1 for y, -1 for no one
        """
        indices = [index for index, value in enumerate(self) if value == num]
        return indices[0] if indices else -1

    def index01(self: Point2D, point: Point2D) -> int:
        """
        Return the index of coordinate of point 1 equals to point 2
        :param point: reference point
        :return: 0 for x, 1 for y, -1 for no one
        """
        # ----------- Method 1 -----------
        # indices = [index for index, (value1, value2) in enumerate(zip(self, point)) if value1 == value2]
        # indices[0] if indices else -1
        # ----------- Method 2 -----------
        return (self - point).index(0)

    def symmetry_about_x(self: Point2D):
        symmetry_matrix = np.array([[1, 0],
                                    [0, -1]])

        return symmetry_matrix @ self

    def symmetry_about_y(self: Point2D):
        symmetry_matrix = np.array([[-1, 0],
                                    [0, 1]])

        return symmetry_matrix @ self

    def symmetry_about_origin(self: Point2D):
        symmetry_matrix = np.array([[-1, 0],
                                    [0, -1]])

        return symmetry_matrix @ self

    def symmetry_about_y_equal_x(self: Point2D):
        symmetry_matrix = np.array([[0, 1],
                                    [1, 0]])

        return symmetry_matrix @ self

    def symmetry_about_y_equal_minus_x(self: Point2D):
        symmetry_matrix = np.array([[0, -1],
                                    [-1, 0]])

        return symmetry_matrix @ self

    def symmetry_about_x_parallel(self: Point2D, axis: int | float = 0.0):
        """
        Symmetric about y-axis, which y does not equal to zero. Here, the value of axis ！= 0

        Steps:
        1. Subtract 1 from x-coordinates
        2. Switch sign of x-coordinates
        3. Add 1 to x-coordinates
        :param point: the point or vector we deal with, normally a 2d vector
        :param axis: the symmetric axis
        :return: point after symmetry
        """
        translate_matrix_1 = np.array([[1, 0, 0],
                                       [0, 1, -axis],
                                       [0, 0, 1]])
        symmetry_matrix = np.array([[1, 0, 0],
                                    [0, -1, 0],
                                    [0, 0, 1]])
        translate_matrix_2 = np.array([[1, 0, 0],
                                       [0, 1, axis],
                                       [0, 0, 1]])

        point_3d = np.ones((3, 1), dtype=np.float64)
        point_3d[0:-1, 0] = np.array(self.tolist())
        new_point_3d = translate_matrix_2 @ symmetry_matrix @ translate_matrix_1 @ point_3d

        return Point2D(new_point_3d[:-1, 0].tolist())

    def symmetry_about_y_parallel(self: Point2D, axis: int | float = 0.0):
        """
        Symmetric about y-axis, which y does not equal to zero. Here, the value of axis ！= 0
        :param point:
        :param axis:
        :return:
        """
        translate_matrix_1 = np.array([[1, 0, -axis],
                                       [0, 1, 0],
                                       [0, 0, 1]])
        symmetry_matrix = np.array([[-1, 0, 0],
                                    [0, 1, 0],
                                    [0, 0, 1]])
        translate_matrix_2 = np.array([[1, 0, axis],
                                       [0, 1, 0],
                                       [0, 0, 1]])
        point_3d = np.ones((3, 1), dtype=np.float64)
        point_3d[0:-1, 0] = np.array(self.tolist())
        new_point_3d = translate_matrix_2 @ symmetry_matrix @ translate_matrix_1 @ point_3d

        return Point2D(new_point_3d[:-1, 0].tolist())


class Coord2D(Point2D):
    ...


if __name__ == '__main__':
    # ==================================== Test RealProperty ====================================
    # num = RealProperty(default=1.0)
    # print(num)
    # ==================================== Test IntProperty ====================================
    # num = IntProperty(default=1)
    # print(num)
    # ==================================== Test RealProperty ====================================
    # num = FloatProperty(default=1)
    # print(num)
    # ==================================== Test Point2D ====================================
    p = Point2D(1, 2)
    print(p)
    ...
