from .estado_reserva import ReservaAtiva, ReservaCancelada, ReservaConcluida

# Padrão Observer para notificar mudanças
class Observer:
    def atualizar(self, reserva):
        raise NotImplementedError()


class EmailNotificador(Observer):
    def atualizar(self, reserva):
        print(f"[Email] Notificação: A reserva foi {reserva.estado.__class__.__name__}.")


class LogReserva(Observer):
    def atualizar(self, reserva):
        print(f"[Log] Estado da reserva alterado para: {reserva.estado.__class__.__name__}")


# Modelos Sala e Reserva
class Sala:
    #evita comflitos de horário entre reservas
    def __init__(self, nome: str):
        self.nome = nome
        self.reservas: list[Reserva] = []

    def verifica_conflito(self, nova_reserva):
        #verifica se a nova reserva conflita com as reservas existentes
        for r in self.reservas:
            if r.data == nova_reserva.data and (nova_reserva.hora_inicial < r.hora_final and nova_reserva.hora_final > r.hora_inicial):
                return True
        return False

    def adicionar_reserva(self, nova_reserva):
        if self.verifica_conflito(nova_reserva):
            raise ValueError(f"Conflito: Sala '{self.nome}' já possui reserva nesse horário.")
        self.reservas.append(nova_reserva)

    def remover_reserva(self, reserva):
        if reserva in self.reservas:
            self.reservas.remove(reserva)

    def __repr__(self):
        return f"Sala({self.nome})"


class Reserva:
    def __init__(self, usuario, sala: Sala, data: str, hora_inicial: str, hora_final: str, nome_materia: str):
        self.usuario = usuario
        self.sala = sala
        self.data = data
        self.hora_inicial = hora_inicial
        self.hora_final = hora_final
        self.nome_materia = nome_materia
        self.ativo = True
        self.estado = ReservaAtiva()
        self.observadores: list[Observer] = []

        # Apenas solicita à sala que inclua esta nova reserva
        self.sala.adicionar_reserva(self)

    def adicionar_observador(self, obs: Observer):
        self.observadores.append(obs)

    def notificar_observadores(self):
        for obs in self.observadores:
            obs.atualizar(self)

    def cancelar(self):
        self.estado.cancelar(self)
        self.notificar_observadores()

    def concluir(self):
        self.estado.concluir(self)
        self.notificar_observadores()

    def modificar(self, data: str, hora_inicial: str, hora_final: str, nome_materia: str):
        """Remove temporariamente, verifica conflito pelo próprio `Sala` e depois grava nova informação."""
        self.sala.remover_reserva(self)

        original = (self.data, self.hora_inicial, self.hora_final, self.nome_materia)

        self.data = data
        self.hora_inicial = hora_inicial
        self.hora_final = hora_final
        self.nome_materia = nome_materia

        try:
            self.sala.adicionar_reserva(self)
        except ValueError:
            # Se houve conflito, faz o rollback
            self.data, self.hora_inicial, self.hora_final, self.nome_materia = original
            self.sala.adicionar_reserva(self)
            raise

        self.notificar_observadores()

    def to_dict(self) -> dict:
        return {
            "usuario": self.usuario.nome,
            "email": self.usuario.email,
            "sala": self.sala.nome,
            "data": self.data,
            "hora_inicial": self.hora_inicial,
            "hora_final": self.hora_final,
            "nome_materia": self.nome_materia,
            "estado": self.estado.__class__.__name__,
            "ativo": self.ativo,
        }


# Proxy para controle de acesso
class ReservaProxy:
    """Verifica se o usuário está cadastrado antes de deixá-la fazer a reserva."""
    def __init__(self, usuarios_cadastrados: list):
        self.usuarios_cadastrados = usuarios_cadastrados

    def fazer_reserva(self, usuario, sala: Sala, data: str, hora_inicial: str, hora_final: str, nome_materia: str) -> Reserva:
        if usuario not in self.usuarios_cadastrados:
            raise PermissionError("Usuário não cadastrado. Reserva negada.")
        return Reserva(usuario, sala, data, hora_inicial, hora_final, nome_materia)
