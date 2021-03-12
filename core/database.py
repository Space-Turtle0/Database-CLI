import logging
import os
from typing import Text
from peewee import *
from discord.enums import ExpireBehavior
from peewee import AutoField, ForeignKeyField, Model, IntegerField, PrimaryKeyField, TextField, SqliteDatabase, DoesNotExist, DateTimeField, UUIDField, IntegrityError
from playhouse.shortcuts import model_to_dict, dict_to_model  # these can be used to convert an item to or from json http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#model_to_dict
from playhouse.sqlite_ext import RowIDField
from datetime import datetime


db = SqliteDatabase("data.db", pragmas={'foreign_keys': 1})

def iter_table(model_dict):
    """Iterates through a dictionary of tables, confirming they exist and creating them if necessary."""
    for key in model_dict:
        if not db.table_exists(key):
            db.connect(reuse_if_open=True)
            db.create_tables([model_dict[key]])
            print(f"Created table '{key}'")
            db.close()

class BaseModel(Model):
    """Base Model class used for creating new tables."""
    class Meta:
        database = db

class MeetingSession(BaseModel):
    id = PrimaryKeyField()
    period = TextField() 
    day = TextField(default = "None")    
    timeStarted = TextField()
    link = TextField()


class Notes(BaseModel):
    id = PrimaryKeyField()
    noteName = TextField(unique=True)
    passwordProtected = TextField(default="FALSE")
    note = TextField()

class HomeWork(BaseModel):
    id = PrimaryKeyField()
    subject = TextField()
    dueDate = TextField()
    notes = TextField(default="NONE GIVEN")


tables = {"meetingsession": MeetingSession, "notes" : Notes, "homework": HomeWork}
iter_table(tables)
