import pytest
from src.models.user import User, Admin, TipoUsuario
from src.models.reserva import ReservaProxy

@pytest.fixture
def proxy_users():
    users = []
    proxy = ReservaProxy(users)
    return users, proxy

def test_criar_user_comum(proxy_users):
    users, proxy = proxy_users
    user = User("Alice", "alice@example.com", "senha123", proxy)
    users.append(user)

    assert user.nome == "Alice"
    assert user.email == "alice@example.com"
    assert user.tipo == TipoUsuario.COMUM
    assert user.reservas == []

def test_criar_user_admin(proxy_users):
    users, proxy = proxy_users
    admin = Admin("Bob", "bob@example.com", "adminpass", proxy)
    users.append(admin)

    assert admin.nome == "Bob"
    assert admin.email == "bob@example.com"
    assert admin.tipo == TipoUsuario.ADMIN

@pytest.mark.parametrize("email", ["invalid", "@nope.com", "user@.com"])
def test_email_invalido_gera_erro(proxy_users, email):
    users, proxy = proxy_users
    with pytest.raises(ValueError):
        User("Test", email, "pass", proxy)
