from estado_reserva import ReservaAtiva

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

# Reserva e Sala
class Reserva:
    def __init__(self, usuario, sala, data, hora_inicial, hora_final, nome_materia):
        self.usuario = usuario
        self.sala = sala
        self.data = data
        self.hora_inicial = hora_inicial
        self.hora_final = hora_final
        self.nome_materia = nome_materia
        self.ativo = True
        self.estado = ReservaAtiva()
        self.observadores = []

    def adicionar_observador(self, obs):
        self.observadores.append(obs)

#State : permitir que um objeto altere seu comportamento quando seu estado interno muda, delegando para classes especificas
    def notificar_observadores(self):
        for obs in self.observadores:
            obs.atualizar(self)

    def cancelar(self):
        self.estado.cancelar(self)
        self.notificar_observadores()

    def concluir(self):
        self.estado.concluir(self)
        self.notificar_observadores()

    def desativar(self):
        if not self.ativo:
            print("Reserva já está desativada.")
            return
        self.ativo = False
        print(f"Reserva em {self.data} {self.hora_inicial}-{self.hora_final} desativada.")
        self.notificar_observadores()

    def to_dict(self) -> dict:
        return {
            "data": self.data,
            "hora_inicial": self.hora_inicial,
            "hora_final": self.hora_final,
            "nome": self.usuario.nome,
            "nome_materia": self.nome_materia,
            "email": self.usuario.email,
            "sala": self.sala,
            "ativo": self.ativo
        }

class Sala:
    def __init__(self, nome):
        self.nome = nome
        self.reservas = []

    def adicionar_reserva(self, reserva):
        for r in self.reservas:
            if r.data == reserva.data and (reserva.hora_inicial < r.hora_final and reserva.hora_final > r.hora_inicial):
                raise Exception("Já existe uma reserva nesse intervalo para esta sala.")
        self.reservas.append(reserva)

    def __repr__(self):
        return f"Sala({self.nome})"

# Proxy para controle de acesso
class ReservaProxy:
    def __init__(self, usuarios_cadastrados):
        self.usuarios_cadastrados = usuarios_cadastrados

    def fazer_reserva(self, usuario, sala, data, hora_inicial, hora_final, nome_materia):
        if not any(u["email"] == usuario.email for u in self.usuarios_cadastrados):
            raise Exception("Usuário não está cadastrado. Reserva negada.")

        nova_reserva = Reserva(usuario, sala, data, hora_inicial, hora_final, nome_materia)
        sala.adicionar_reserva(nova_reserva)
        return nova_reserva
