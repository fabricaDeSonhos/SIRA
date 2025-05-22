class EstadoReserva:
    def cancelar(self, reserva):
        raise NotImplementedError()

    def concluir(self, reserva):
        raise NotImplementedError()

class ReservaAtiva(EstadoReserva):
    def cancelar(self, reserva):
        reserva.estado = ReservaCancelada()
        print("Reserva cancelada com sucesso.")

    def concluir(self, reserva):
        reserva.estado = ReservaConcluida()
        print("Reserva concluída com sucesso.")

class ReservaCancelada(EstadoReserva):
    def cancelar(self, reserva):
        print("Reserva já está cancelada.")

    def concluir(self, reserva):
        print("Não é possível concluir uma reserva cancelada.")

class ReservaConcluida(EstadoReserva):
    def cancelar(self, reserva):
        print("Não é possível cancelar uma reserva concluída.")

    def concluir(self, reserva):
        print("Reserva já está concluída.")


