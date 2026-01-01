"""
Type hint let us add type information to python code, which can help us write self-documenting code,
catch bugs earlier and get better IDE completions.

In python, type hinting doesn't give error on type mismatch. We need type checker for that.
 - mypy -> uvx mypy <file_name>

 Instead of age: int | None -> age: Optional[int] (older way)
"""

from typing import NewType, Tuple, TypedDict

RGB = NewType("RGB", Tuple[int, int, int])
HSL = NewType("HSL", Tuple[int, int, int])

# type alias -> older version
UserReturnType = dict[str, str | int | RGB | None]

# type alias with python new version
type UserReturnTypeNew = dict[str, str | int | None]

# This allows to define type of each dict properties
class User(TypedDict):
    first_name: str
    last_name: str
    email: str
    age: int | None
    fav_color: RGB | None


def create_user(first_name: str, last_name: str, age: int | None = None,
                fav_color: RGB | None = None) -> User:
    email = f"{first_name.lower()}_{last_name.lower()}@example.com"
    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "age": age,
        "fav_color": fav_color,
    }


user1 = create_user("John", "Doe")
user2 = create_user("Oliver", "Doe", age=22, fav_color=RGB((200,90,78)))
