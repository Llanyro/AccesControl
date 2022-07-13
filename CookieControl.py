import uuid


class SessionRegister:
    # region Varaibles
    __database: dict        # Lista de claves y valores del controlador

    # endregion
    # region Functions
    def __init__(self):
        self.__database = {}

    def get_uuid(self, key: str) -> str:
        """
        Busca en la db el uuid guardado de una key dada
        """
        result: str = ""
        tmp = self.__database.get(key)
        if tmp is not None:
            result = tmp
        return result

    def get_key_by_uuid(self, uuid_asociated: str) -> str:
        """
        Busca en la db el uuid guardado de una key dada
        """
        result: str = ""
        if uuid_asociated in self.__database.values():
            result = list(self.__database.keys())[list(self.__database.values()).index(uuid_asociated)]
        return result

    def add_key(self, key: str) -> str:
        """
        Si existe devuelve el uuid anterior
        Si no existe, genera un uuid nuevo y lo devuelve
        """
        result: str = self.get_uuid(key)
        if result.__len__() == 0:
            result = str(uuid.uuid4())
            # If contains the uuid generated
            while self.contains_uuid(result):
                result = str(uuid.uuid4())
            self.__database.update({key: result})
        return result

    def delete_key(self, key: str) -> bool:
        result: bool = False
        if key in self.__database:
            del self.__database[key]
            result = True
        return result

    def delete_uuid(self, uuid_asociated: str) -> bool:
        result: bool = False
        key: str = self.get_key_by_uuid(uuid_asociated)
        if key.__len__() > 0:
            self.delete_key(key)
            result = True
        return result

    def contains_uuid(self, uuid_asociated: str) -> bool:
        return self.get_key_by_uuid(uuid_asociated).__len__() != 0

    def contains_key(self, key: str) -> bool:
        return self.get_uuid(key).__len__() != 0

    def print_list(self):
        for i in self.__database:
            print(f"{i}: {self.__database[i]}")

    # endregion
