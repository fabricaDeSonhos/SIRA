
class DuplicateRoomError(Exception):
    """
    Exceção lançada quando se tenta criar uma sala
    com um nome que já existe no banco de dados.
    """
    def __init__(self, message: str):
        super().__init__(message)
