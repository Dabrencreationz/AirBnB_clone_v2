#!/usr/bin/python3
"""
Contains the DBStorage which creates a Database Engine
"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """This class manages storage of hbnb models in a mysql database"""
    __engine = None
    __session = None

    __env = {
            'user': getenv('HBNB_MYSQL_USER', default=None),
            'passwd': getenv('HBNB_MYSQL_PWD', default=None),
            'host': getenv('HBNB_MYSQL_HOST', default=None),
            'database': getenv('HBNB_MYSQL_DB', default=None),
            'env': getenv('HBNB_ENV', default=None)
                }

    __classes = {
            'State': State, 'City': City, 'User': User
                }

    def __init__(self):
        """Initializes an instance of the class"""
        env = self.__env
        self.__engine = create_engine("\
mysql+mysqldb://{}:{}@{}/{}".format(env["user"], env["passwd"], env["host"],
                                    env["database"]), pool_pre_ping=True)
        if env["env"] == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in the database"""
        objects = {}
        if cls is not None:
            cls_objs = self.__session.query(cls).all()
            for cls_obj in cls_objs:
                obj_id = cls.__name__ + '.' + cls_obj.id
                objects[obj_id] = cls_obj
        else:
            for key, value in self.__classes.items():
                cls_objs = self.__session.query(value).all()
                for cls_obj in cls_objs:
                    obj_id = key + '.' + cls_obj.id
                    objects[obj_id] = cls_obj
        return objects

    def new(self, obj):
        """adds an object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes an object from the current database session if it is not \
None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """creates all tables in the database and creates the current \
database session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
