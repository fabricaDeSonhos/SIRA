# Em policies/reservation_policy.py

from src.models.user_models import User, Admin
from src.models.reserva_models import Reserva

class ReservaPolicy:
    """
    Contém todas as regras de autorização para o recurso Reserva.
    Os métodos levantam PermissionError se a ação não for permitida.
    """

    def _is_user_active(self, user: User):
        """Regra universal: o usuário deve estar ativo."""
        if not user.is_active:
            raise PermissionError("A sua conta está inativa. Ação não permitida.")

    def can_create(self, user: User, reservation_data: dict):
        """Verifica se o usuário pode criar uma reserva com os dados fornecidos."""
        self._is_user_active(user)

        # Regra: Apenas admins podem criar reservas fixas.
        is_trying_to_create_fixed = reservation_data.get("is_fixed", False)
        if is_trying_to_create_fixed and not isinstance(user, Admin):
            raise PermissionError("Apenas administradores podem criar reservas fixas.")
        
        return True # Se nenhuma exceção foi levantada, a ação é permitida.

    def can_view(self, user: User, reservation: Reserva):
        """Verifica se o usuário pode visualizar uma reserva específica."""
        self._is_user_active(user)

        # Regra: Admins podem ver tudo. Usuários comuns só podem ver as próprias reservas.
        if isinstance(user, Admin):
            return True
        
        if user.id != reservation.user_id:
            raise PermissionError("Você não tem permissão para visualizar esta reserva.")
        
        return True

    def can_update(self, user: User, reservation: Reserva):
        """Verifica se o usuário pode atualizar uma reserva específica."""
        self._is_user_active(user)

        # Regra: Admins podem atualizar tudo. Usuários comuns só podem atualizar as próprias reservas.
        if isinstance(user, Admin):
            return True # Admins têm passe livre
        
        if user.id != reservation.user_id:
            raise PermissionError("Você não tem permissão para atualizar esta reserva.")

        return True

    def can_delete(self, user: User, reservation: Reserva):
        """Verifica se o usuário pode deletar uma reserva específica."""
        # A lógica para deletar e atualizar costuma ser a mesma.
        self.can_update(user, reservation)
        return True