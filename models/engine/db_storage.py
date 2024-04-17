#!/usr/bin/python3
""" DB Storage engine """
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import create_engine
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ Represents a database storage engine """
    __engine = None
    __session = None

    def __init__(self):
        """ Initializes the class attributes """
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on the current database session """
        dict = {}

        if cls:
            if type(cls) is str:
                cls = eval(cls)

            value = self.__session.query(cls)
            for attr in value:
                key = "{}.{}".format(type(attr).__name__, attr.id)
                dict[key] = attr
        else:
            lists = [User, State, City, Amenity, Place, Review]

            for list in lists:
                value = self.__session.query(list)
                for attr in value:
                    key = "{}.{}".format(type(attr).__name__, attr.id)
                    dict[key] = attr

        return dict

    def new(self, obj):
        """ add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ create all tables in the database """
        Base.metadata.create_all(self.__engine)
        session_make = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_make)
        self.__session = Session()
