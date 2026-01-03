from pydantic import BaseModel, ValidationError
from datetime import datetime


# Pydantic will use this property to validate the data at runtime.
class User(BaseModel):
    uid: int
    username: str  # These are required field as we don't pass default value. Pydantic will require these to be passed in when we create a user instance.
    email: str
    bio: str = ""
    is_active: bool = True  # If we don't pass explicitly then it will take this default value.

    full_name: str | None = None  # Optional value without default value.
    verified_at: datetime | None = None


user = User(uid = 23,username="sk", email="email")
print(user)
