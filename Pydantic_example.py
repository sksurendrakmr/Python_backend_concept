from pydantic import BaseModel, ValidationError
from datetime import datetime

'''
    Model instances are mutable by default and also by default they don't revalidate when we change a field.
    We can change this default behaviour in model configuration.
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
