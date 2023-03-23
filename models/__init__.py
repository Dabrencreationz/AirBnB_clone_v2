#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import getenv
from models.engine.file_storage import FileStorage
import models.engine.db_storage as db_storage

DBStorage = db_storage.DBStorage
storage_type = getenv("HBNB_TYPE_STORAGE", default=None)

if storage_type == "db":
    storage = DBStorage()
else:
    storage = FileStorage()
storage.reload()
