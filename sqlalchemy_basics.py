'''
Sqlalchemy has two packages:
    - SQLAlchemy Core -> Database toolkit
    - SQLAlchemy ORM -> Deal with ORM

    SQLAlchemy Core deal with connection.
    SQLAlchemy ORM deal with session.

    This way of using SQLAlchemy is to run raw SQL directly. But this is now SQLAlchemy is used for.

    With SQLAlchemy, either we used its core package where we can use functions and metadata to create everything
    in the database easily, or we use an ORM(Object Relational Mapper) to map python classes to database tables.


'''
from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///mydatabase.db', echo=True)
db_connection = engine.connect()

db_connection.execute(text("CREATE TABLE IF NOT EXISTS people (name str, age int)"))
db_connection.commit()

from sqlalchemy.orm import Session

session = Session(engine)

session.execute(text("INSERT INTO people (name, age) VALUES ('john', 27);"))
session.commit()