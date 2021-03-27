from sqlalchemy import create_engine


class AbstractService:

    conn_string = "mysql+mysqlconnector://db_user:db_password@127.0.0.1:3306/common"

    def __init__(self) -> None:
        self.engine = create_engine(self.conn_string, echo=True)

    async def insert(self, query):
        with self.engine.connect() as conn:
            conn.execute(query)

    async def select(self, query):
        with self.engine.connect() as conn:
            return conn.execute(query).fetchone()
