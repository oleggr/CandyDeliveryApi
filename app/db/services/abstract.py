from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class AbstractService:

    conn_string = "mysql+mysqlconnector://db_user:db_password@127.0.0.1:3306/common"

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
