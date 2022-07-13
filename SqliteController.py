from sqlite3 import connect, Connection, Cursor


class SQLiteController:
    """
    This class is a controller for sesions and users
    That means, controls if a user is registered or not
    And checks if have a cookie session
    """
    __conn = None
    __cursor = None

    # region Class
    def __init__(self, database_name: str, check_same_thread: bool):
        self.__conn = connect(database_name, check_same_thread=check_same_thread)
        self.__cursor = self.__conn.cursor()

    def preparar_db(self, table: str, params: str):
        try:
            self.__cursor.execute(f"CREATE TABLE {table} {params}")
        except:
            pass

    def get_list(self, table: str, colum: int) -> list:
        result: list = []
        for row in self.__cursor.execute(f"SELECT * FROM {table}"):
            result.append(row[colum])
        return result

    def get_table(self, table: str) -> list:
        """
        Returns list of lists -> A table
        :param table: Table name
        :return:
        """
        result: list = []
        for row in self.__cursor.execute(f"SELECT * FROM {table}"):
            tmp: list = []
            for cell in row:
                tmp.append(cell)
            result.append(tmp)
        return result

    @property
    def conn(self) -> Connection:
        return self.__conn

    @property
    def cursor(self) -> Cursor:
        return self.__cursor

    # endregion

