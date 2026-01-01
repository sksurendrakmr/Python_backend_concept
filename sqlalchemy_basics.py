'''
Sqlalchemy has two packages:
    - SQLAlchemy Core -> Database toolkit
    - SQLAlchemy ORM -> Deal with ORM

    SQLAlchemy Core deal with connection.
    SQLAlchemy ORM deal with session.


'''
from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///mydatabase.db', echo=True)
db_connection = engine.connect()

db_connection.execute(text("CREATE TABLE IF NOT EXISTS people (name str, age int)"))
db_connection.commit()

