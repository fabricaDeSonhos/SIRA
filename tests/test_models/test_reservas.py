
import pytest
from src.models.reserva import Sala, ReservaProxy, Reserva
from src.models.user    import User

@pytest.fixture
def sala():
    return Sala("Lab101")

@pytest.fixture
def proxy_sala():
    users = []
    proxy = ReservaProxy(users)
    return users, proxy

@pytest.fixture
def usuario(proxy_sala):
    users, proxy = proxy_sala
    u = User("Carol", "carol@example.com", "pw", proxy)
    users.append(u)
    return u


def test_fazer_reserva_adiciona_em_sala(usuario, sala):
    res = usuario.fazer_reserva(sala, "2025-06-20", "08:00", "10:00", "Math")
    assert res in sala.reservas
    assert res.usuario == usuario


def test_conflito_gera_erro(usuario, sala):
    usuario.fazer_reserva(sala, "2025-06-21", "09:00", "11:00", "Physics")
    with pytest.raises(ValueError):
        usuario.fazer_reserva(sala, "2025-06-21", "10:00", "12:00", "Chemistry")


def test_cancelar_reserva_remove(usuario, sala):
    res = usuario.fazer_reserva(sala, "2025-06-22", "14:00", "16:00", "History")
    usuario.cancelar_reserva(res)
    assert res not in usuario.reservas
    assert res not in sala.reservas


def test_modificar_reserva(usuario, sala):
    res = usuario.fazer_reserva(sala, "2025-06-23", "10:00", "12:00", "Geo")
    usuario.modificar_reserva(res, "2025-06-23", "11:00", "13:00", "Biology")
    assert res.hora_inicial == "11:00"
    assert res.nome_materia == "Biology"
