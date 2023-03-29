#!/usr/bin/python3
""" holds class Place"""
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from models.review import Review
import models

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'), primary_key=True))


class Place(BaseModel, Base):
    """Representation of Place """
    __tablename__ = 'places'
    city_id = Column(String(60),
                     ForeignKey("cities.id"),
                     nullable=False)
    user_id = Column(String(60),
                     ForeignKey('users.id'),
                     nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    reviews = relationship('Review', backref='place',
                           cascade='all, delete-orphan')

    amenities = relationship("Amenity", secondary=place_amenity,
                             viewonly=False,
                             back_populates="place_amenities")

    if getenv("HBNB_TYPE_STORAGE", default=None) != "db":
        @property
        def reviews(self):
            """
            Getter of all review linked to Place instance
            """
            from models.review import Review
            review_objs = [value for value in storage.all(Review).values()
                           if value.place_id == self.id]
            return review_objs

        @property
        def amenities(self):
            from models.amenity import Amenity
            values_amenity = models.storage.all(Amenity).values()
            list_amenity = []
            for amenity_id in self.amenity_ids:
                for amenity in values_amenity:
                    if amenity.id == amenity_id:
                        list_amenity.append(amenity)
            return list_amenity

        @amenities.setter
        def amenities(self, obj):
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
