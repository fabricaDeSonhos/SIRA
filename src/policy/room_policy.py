# /policies/room_policy.py (Novo arquivo)

from ..models.user_models import User, Admin

class RoomPolicy:
    """
    Regras de autorização para o recurso Sala.
    Apenas Admins podem realizar ações de escrita.
    """

    def can_manage(self, user: User):
        """Verifica se o usuário pode criar, alterar ou deletar salas."""
        if not isinstance(user, Admin):
            raise PermissionError("Apenas administradores podem gerenciar salas.")
        return True
    
    # A visualização de salas é pública, não precisa de um método específico.