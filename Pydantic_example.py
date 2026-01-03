from functools import partial
from typing import Literal, Annotated

from pydantic import BaseModel, ValidationError, Field
from datetime import datetime, UTC

'''
    Model instances are mutable by default and also by default they don't revalidate when we change a field.
    We can change this default behaviour in model configuration.
    
    https://gist.github.com/CoreyMSchafer/26fbfae9fb2ad293cc431530e8932855
'''


# Pydantic will use this property to validate the data at runtime.
class User(BaseModel):
    uid: int
    username: str  # These are required field as we don't pass default value. Pydantic will require these to be passed in when we create a user instance.
    email: str
    bio: str = ""
    is_active: bool = True  # If we don't pass explicitly then it will take this default value.

    full_name: str | None = None  # Optional value without default value.
    verified_at: datetime | None = None


user = User(uid=23, username="sk", email="email")
print(user)

# Modifying and accessing data
print(user.username)  # access

# setting of value
user.bio = "123"
print(user.bio)

# to convert pydantic model to dictionary
print(user.model_dump())

# to get JSON
print(user.model_dump_json(indent=2))  # indent format the JSON with 2 spaces.

'''
    model_dump() and model_dump_json() are useful when we need to serialize our model for storage or sending over a network.
    Serialize means converting the Python object into a simple format that can be easily saved to a file or sent to different systems.
'''

# ------------- WHAT IF VALIDATION FAIL -------------
'''
    Pydantic catches multiple errors at once.
    uid will not be in the error list if validation fails. This is because Pydantic has type coercion enabled by default.
    E.g. if we try to assign string in place of int, it will try to convert types when it make sense to do so.
    
    uid = "123" -> pydantic will do type coercion
    uid = "Test" -> pydantic will include uid in validation error list.
'''

try:
    user1 = User(uid="Test", username=None, email=123)
    print(user1.model_dump_json(indent=2))
except ValidationError as e:
    print(e)

# ------------------- Pydantic types and how to validate it ---------
'''
    Pydantic support all the standard python types that we would expect.
    - int
    - bool
    - str
    - float
    - list
    - dictionary
    - tuple
    - set
    - datetime etc.
    
    We can use Union to tell that a field can be one of several types and we can use Optional to allow None values.
    Even we can use literal types to specify exact values that are allowed.
    
    funcTool partial let us prefill some arguments to a function. So it allows us to pass in a function and some argument
    and returns a new unexpected function that is the original function with those specific arguments already set.
'''


class BlogPost(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    content: Annotated[str, Field(min_length=10)]
    view_count: int = 0
    is_published: bool = False
    tags: list[str] = Field(
        default_factory=list)  # default_factory is a function that get called to create a new default value each time we create an instance
    # created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    created_at: datetime = Field(default_factory=partial(datetime.now, tz=UTC))
    author_id: int | str
    status: Literal["draft", "published", "archived"] = "draft"
    slug: Annotated[str, Field(pattern=r"^[a-z0-9-]+$")]


# ------------ ADDING CONSTRAINTS TO FIELD -----
'''
    We already been using Field for things like default_factory.
    We can use it add constraints like minimum and maximum values, Length requirements and patterns etc.
    
    From Pydantic version 2, the recommended way to add constraints is using the annotated type from python typing modules.
    
    Annotated -> way to add metadata to the current type.
'''


class EmployeePost(BaseModel):
    eid: Annotated[int, Field(gt=0)]
    employee_name: Annotated[str, Field(min_length=3, max_length=20)]
    age: Annotated[int, Field(ge=15, le=70)]
