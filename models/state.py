#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    name = Column(String(128), nullable=False)

    cities = relationship("City", backref="state",
                          cascade="all, delete-orphan")

    if getenv("HBNB_TYPE_STORAGE", default=None) != "db":
        @property
        def cities(self):
            """
            Getter for cities associated with state
            """
            from models.city import City
            city_objs = [value for value in models.storage.all(City).values()
                         if value.state_id == self.id]
            return city_objs
