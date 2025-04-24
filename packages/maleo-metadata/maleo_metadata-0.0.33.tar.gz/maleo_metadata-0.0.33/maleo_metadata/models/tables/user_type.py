from sqlalchemy import Column, Integer, String
from maleo_foundation.db.table import BaseTable
from maleo_metadata.utils.db import MaleoMetadataDatabaseManager

class UserTypesTable(MaleoMetadataDatabaseManager.Base, BaseTable):
    __tablename__ = "user_types"
    order = Column(name="order", type_=Integer)
    key = Column(name="key", type_=String(20), unique=True, nullable=False)
    name = Column(name="name", type_=String(20), unique=True, nullable=False)