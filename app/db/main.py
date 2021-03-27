# import os
# from sqlalchemy import create_engine
#
# from app.db.schema import couriers_table

# conn_string = os.getenv('DB_CONNECTION', "mysql+mysqlconnector://db_user:db_password@db_domain:3306/common")
#
# engine = create_engine(conn_string, echo=True)


# with engine.connect() as conn:
#
#     # query = couriers_table.insert().values(
#     #     {'courier_id': 1, 'courier_type': 'foot'},
#     # )
#     #
#     # conn.execute(query)
#     #
#     # data = conn.execute('SELECT 1').fetchone()
#
#     query = couriers_table.select()
#
#     data = conn.execute(query).fetchone()

class DbConfig:
    user = 'root'
    password = 'db_password'
    # host = 'db_domain'
    host = '127.0.0.1'
    port = 3306
    default_db = 'common'
    driver = 'mysql+mysqlconnector'

    conn_string_pattern = '{}://{}:{}@{}:{}/{}'

    @staticmethod
    def get_conn_string(db=default_db):
        return DbConfig.conn_string_pattern.format(
            DbConfig.driver,
            DbConfig.user,
            DbConfig.password,
            DbConfig.host,
            DbConfig.port,
            db
        )
