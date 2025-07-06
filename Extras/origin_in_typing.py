from typing_extensions import get_origin
from typing import Callable, Union, Literal


#! Yahan None nhi ayega
print(get_origin(tuple[str]))
print(get_origin(Callable[[int, int], int]))
print(get_origin(Union[str, int]))
print(get_origin(Literal["red", "blue", "green"]))


#! Yahan None ayega
print(get_origin(str))
print(get_origin(int))
print(get_origin(float))