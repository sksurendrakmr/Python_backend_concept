'''
Sqlalchemy has two packages:
    - SQLAlchemy Core -> Database toolkit
    - SQLAlchemy ORM -> Deal with ORM

    SQLAlchemy Core deal with connection.
    SQLAlchemy ORM deal with session.

    This way of using SQLAlchemy is to run raw SQL directly. But this is now SQLAlchemy is used for.

    With SQLAlchemy, either we used its core package where we can use functions and metadata to create everything
    in the database easily, or we use an ORM(Object Relational Mapper) to map python classes to database tables.

    metadata -> It will keep tracks of all the information necessary to create table columns, constraints etc.
    When we work with SQLAlchemy Core, we have to work with metadata object.
    When we work with SQLAlchemy ORM, we work with a declarative base.


'''
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, insert, ForeignKey

engine = create_engine('sqlite:///mydatabase.db', echo=True)

metadata = MetaData()

people = Table(
    'people',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('age', Integer, nullable=False)
)

things = Table(
    'things',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('description', String(500), nullable=False),
    Column('value', Float),
    Column('owner', Integer, ForeignKey('people.id')),
)

metadata.create_all(engine)
db_connection = engine.connect()


insert_statement = people.insert().values(name='Andrew', age=20)
#M2
insert_statement2 = insert(people).values(name='Oliver', age=20)
results = db_connection.execute(insert_statement)
db_connection.commit()

# select data
select_statement = people.select().where(people.c.age > 20)
result = db_connection.execute(select_statement)

for row in result.fetchall():
    print(row)

# update statement

update_statement = people.update().where(people.c.age > 20).values(age=50)
updatedResult = db_connection.execute(update_statement)
db_connection.commit()

# delete statement
delete_statement = people.delete().where(people.c.age > 40)
deleteResult = db_connection.execute(delete_statement)
db_connection.commit()

