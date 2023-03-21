#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    name = Column(String(128), nullable=False)

    cities = relationship("City", back_populates="state",
                          cascade="all, delete-orphan")

    @property
    def cities(self):
        """
        Getter for cities associated with state
        """
        city_objs = [value for value in storage.all(City).values()
                     if value.state_id == self.id]
        return city_objs
