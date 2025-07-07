#talvez adiconar uma iterface Iuser
class Iuser_service():
    def __init__(self, id: str, name: str, email: str, hashed_password: str, is_active: bool = True):
        self.id = id
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active
    
    def create_user(self):
        raise NotImplementedError("Este método deve ser implementado por subclasses.")
    
    def atualizar_user(self):
        raise NotImplementedError("Este método deve ser implementado por subclasses.")

    def get_user(self):
        raise NotImplementedError("Este método deve ser implementado por subclasses.")

        

class User_service():
    def __init__(self, id: str, name: str, email: str, hashed_password: str, is_active: bool = True):
        self.id = id
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active

    def create_user(self):
        # Implementar lógica para criar um usuário no banco de dados
        pass

    def atualizar_user(self):
        # Implementar lógica para atualizar os dados do usuário no banco de dados
        pass


    def get_user(self):
        # Implementar lógica para obter os dados do usuário do banco de dados
        pass

    class Admin_service(User_service):
        def __init__(self, id: str, name: str, email: str, hashed_password: str, is_active: bool = True):
            super().__init__(id, name, email, hashed_password, is_active)

        def create_admin(self):
            # Implementar lógica para criar um administrador no banco de dados
            pass

        def get_admin(self):
            # Implementar lógica para obter os dados do administrador do banco de dados
            pass