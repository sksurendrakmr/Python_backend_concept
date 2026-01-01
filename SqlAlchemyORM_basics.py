from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///memory.db')

Base = declarative_base()


class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer)

    things = relationship('Thing', back_populates='people')


class Thing(Base):
    __tablename__ = 'things'
    id = Column(Integer, primary_key=True)
    description = Column(String(500), nullable=False)
    value = Column(Float)
    owner = Column(Integer, ForeignKey('people.id'))

    people = relationship('People', back_populates='things')


# setup
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# create table
new_person = People(name='John', age=21)
session.add(new_person)
session.flush()  # This will add new_person temporary somewhere and give id. Note: This will not save the data to DB.

new_thing = Thing(description='My favorite thing', value=500, owner=new_person.id)
session.add(new_thing)

session.commit()
