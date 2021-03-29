from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.config import DbConfig


class AbstractService:

    conn_string = DbConfig.get_conn_string()

    def __init__(self) -> None:
        self.engine = create_engine(self.conn_string, echo=True)

    async def execute(self, query):
        with self.engine.connect() as conn:
            conn.execute(query)

    async def select(self, query):
        with self.engine.connect() as conn:
            return conn.execute(query).fetchone()

    async def get_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()
