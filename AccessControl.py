from hashlib import sha3_256
from .SqliteController import SQLiteController
from .CookieControl import SessionRegister


class AccessController:
    """
    This class is a controller for sesions and users
    That means, controls if a user is registered or not
    And checks if have a cookie session
    """
    __sqlite: SQLiteController
    __cookie_database: SessionRegister
    __USER_TABLE: str = "users"
    __table_params: list = ["email", "password"]

    def __init__(self, database_name: str, check_same_thread: bool):
        self.__sqlite = SQLiteController(database_name, check_same_thread)
        self.__cookie_database = SessionRegister()
        self.__sqlite.preparar_db(self.__USER_TABLE, f"({self.__table_params[0]} text, {self.__table_params[1]} text)")

    # region SQLite control
    def __email_and_password_check(self, email: str, password: str) -> bool:
        """
        True if exist in db
        False if not
        """
        return self.__sqlite.cursor.execute(
            f"SELECT * FROM {self.__USER_TABLE} where {self.__table_params[0]}='{email}' and {self.__table_params[1]}='{sha3_256(password.encode('utf8')).hexdigest()}'"
        ).fetchone() is not None

    def __email_exist(self, email: str) -> bool:
        """
        True if exist in db
        False if not
        """
        return self.__sqlite.cursor.execute(
            f"SELECT * FROM {self.__USER_TABLE} where {self.__table_params[0]}='{email}'"
        ).fetchone() is not None

    def __add_new_user(self, email: str, password: str, commit: bool) -> bool:
        """
        Precondition!!!
        User __email_exist() before this!!!
        """
        result: bool = True
        try:
            self.__sqlite.cursor.execute(f"INSERT INTO {self.__USER_TABLE} VALUES ('{email}', '{sha3_256(password.encode('utf8')).hexdigest()}')")
            if commit:
                self.__sqlite.conn.commit()
        except:
            result = False
        return result

    # endregion

    def login(self, email: str, password: str) -> (bool, str):
        """
        Search for user
        Returs if user is added, and the uuid generated for session
        """
        uuid: str = ""
        result: bool = False

        # If user and password matches
        if self.__email_and_password_check(email, password):
            uuid = self.__cookie_database.add_key(email)
            result = True
        return result, uuid

    def signin(self, email: str, password: str) -> (bool, str):
        """
        Adds new user
        Returs if user is added, and the uuid generated for session
        Return False if user already exist
        """
        uuid: str = ""
        result: bool = False

        # If email doesnt exist
        if not self.__email_exist(email):
            # If everything is ok
            if self.__add_new_user(email, password, True):
                uuid = self.__cookie_database.add_key(email)
                result = True
        return result, uuid

    def logout(self, cookie: str) -> bool:
        return self.__cookie_database.delete_uuid(cookie)

    def is_logged(self, cookie: str) -> bool:
        return self.__cookie_database.contains_uuid(cookie)

    def print_cookies(self) -> None:
        self.__cookie_database.print_list()

    def printDB(self) -> None:
        for i in self.__sqlite.get_table(self.__USER_TABLE):
            for j in i:
                print(j, end=" ")
            print("\n", end="")


if __name__ == "__main__":
    session = AccessController("users.db", True)
    print("Signin:", session.signin("Llanyro", "Password"))
    print("Login:", session.login("Llanyro", "Password"))
    session.print_cookies()
    session.printDB()


