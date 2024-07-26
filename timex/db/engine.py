from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from timex.db.models import Base


class Database:
    DB_PATH = "timex.db"
    DB_ENGINE = "sqlite"

    def __init__(self) -> None:
        self.start_engine()
        self._connection = self._engine.connect()

        session = sessionmaker(bind=self._engine)
        self._session = session()

    def _database_string(self) -> str:
        return f"{self.DB_ENGINE}///{self.DB_PATH}"

    def start_engine(self) -> None:
        self._engine = create_engine(self._database_string(), echo=False)

    def create_schema(self) -> None:
        Base.metadata.create_all(self._engine)
