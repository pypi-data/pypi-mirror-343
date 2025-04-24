from sqlalchemy.orm import declarative_base
from maleo_foundation.db.manager import DatabaseManager
from maleo_foundation.db.table import BaseTable

class MaleoMetadataDatabaseManager(DatabaseManager):
    Base = declarative_base(cls=BaseTable)
    metadata = Base.metadata