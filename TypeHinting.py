"""
Type hint let us add type information to python code, which can help us write self-documenting code,
catch bugs earlier and get better IDE completions.

In python, type hinting doesn't give error on type mismatch. We need type checker for that.
 - mypy -> uvx mypy <file_name>

 Instead of age: int | None -> age: Optional[int] (older way)


 TypeVar -> It could be any type, but it will be same type throughout.
"""
import random
from typing import NewType, Tuple
from dataclasses import dataclass

RGB = NewType("RGB", Tuple[int, int, int])
HSL = NewType("HSL", Tuple[int, int, int])

# type alias -> older version
UserReturnType = dict[str, str | int | RGB | None]

# type alias with python new version
type UserReturnTypeNew = dict[str, str | int | None]

#we are returning class, this way we have a lot of access to different method
@dataclass()
class User:
    first_name: str
    last_name: str
    email: str
    age: int | None = None
    fav_color: RGB | None = None


def create_user(first_name: str, last_name: str, age: int | None = None,
                fav_color: RGB | None = None) -> User:
    email = f"{first_name.lower()}_{last_name.lower()}@example.com"
    return User(first_name, last_name, email, age, fav_color)



user1 = create_user("John", "Doe")
user2 = create_user("Oliver", "Doe", age=22, fav_color=RGB((200,90,78)))



def random_choice[T](items: list[T]) -> T:
    return random.choice(items)