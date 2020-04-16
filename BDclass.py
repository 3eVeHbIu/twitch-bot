import mysql.connector


class ConnectionError(Exception):
    pass


class CredintialsError(Exception):
    pass


class SQLError(Exception):
    pass


class UseDatabase:
    def __init__(self, dbconfig: dict) -> None:
        self.config = dbconfig

    def __enter__(self) -> 'cursor':
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except mysql.connector.errors.InterfaceError as err:
            raise ConnectionError(err)
        except mysql.connector.errors.ProgrammingError as err:
            raise CredintialsError(err)

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()
        self.conn.close()
        self.cursor.close()
        if exc_type is mysql.connector.errors.ProgrammingError:
            raise SQLError(exc_value)
        elif exc_type:
            raise exc_type(exc_value)
