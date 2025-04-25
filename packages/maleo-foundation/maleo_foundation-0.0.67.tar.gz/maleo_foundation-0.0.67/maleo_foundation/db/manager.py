from sqlalchemy import Engine, MetaData
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import declarative_base

class DatabaseManager:
    Base:DeclarativeMeta = declarative_base()  #* Correct way to define a declarative base

    #* Explicitly define the type of metadata
    metadata:MetaData = Base.metadata

    @classmethod
    def initialize(cls, engine:Engine):
        """Creates the database tables if they do not exist."""
        cls.metadata.create_all(engine)