import os
from sqlalchemy import create_engine


conn_string = os.getenv('DB_CONNECTION')

engine = create_engine(conn_string, echo=True)

with engine.connect() as conn:
    data = conn.execute('SELECT 1').fetchone()

