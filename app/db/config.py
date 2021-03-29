class DbConfig:
    user = 'root'
    password = 'db_password'
    host = 'db_domain'
    # host = '127.0.0.1'
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
