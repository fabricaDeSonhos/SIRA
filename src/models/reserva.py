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
    def __init__(self, nome: str):
        self.nome = nome
        self.reservas: list[Reserva] = []

    def adicionar_reserva(self, reserva):
        # Garante que não haja conflito de horários
        for r in self.reservas:
            if r.data == reserva.data and (reserva.hora_inicial < r.hora_final and reserva.hora_final > r.hora_inicial):
                raise ValueError(f"Conflito: Sala '{self.nome}' já possui reserva nesse horário.")
        self.reservas.append(reserva)

    def remover_reserva(self, reserva):
        if reserva in self.reservas:
            self.reservas.remove(reserva)

    def __repr__(self):
        return f"Sala({self.nome})"

class Reserva:
    def __init__(self, usuario, sala: Sala, data: str, hora_inicial: str, hora_final: str, nome_materia: str):
        self.usuario = usuario        # link unidirecional: reserva sabe seu usuário
        self.sala = sala              # reserva vinculada a uma sala
        self.data = data
        self.hora_inicial = hora_inicial
        self.hora_final = hora_final
        self.nome_materia = nome_materia
        self.ativo = True
        self.estado = ReservaAtiva()
        self.observadores: list[Observer] = []
        # ao criar, registra na sala
        sala.adicionar_reserva(self)

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
        # atualiza dados, garantindo checagem de conflitos na sala
        # remove temporariamente desta sala, testa e reinsere
        self.sala.remover_reserva(self)
        original = (self.data, self.hora_inicial, self.hora_final)
        self.data = data
        self.hora_inicial = hora_inicial
        self.hora_final = hora_final
        self.nome_materia = nome_materia
        try:
            self.sala.adicionar_reserva(self)
        except ValueError as e:
            # rollback em caso de conflito
            self.data, self.hora_inicial, self.hora_final = original
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
    def __init__(self, usuarios_cadastrados: list):
        self.usuarios_cadastrados = usuarios_cadastrados

    def fazer_reserva(self, usuario, sala: Sala, data: str, hora_inicial: str, hora_final: str, nome_materia: str) -> Reserva:
        if usuario not in self.usuarios_cadastrados:
            raise PermissionError("Usuário não cadastrado. Reserva negada.")
        reserva = Reserva(usuario, sala, data, hora_inicial, hora_final, nome_materia)
        return reserva

    # admin e comum podem cancelar ou modificar via atributos da reserva
