# scripts/demo.py
import sys, os
# adiciona diretório raiz (padrões2) ao path para imports absolutos funcionarem
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.models.reserva import Sala, ReservaProxy
from src.models.user import User, Admin

def main():
    usuarios = []
    proxy    = ReservaProxy(usuarios)

    alice = User("Alice", "alice@ex.com", "1234", proxy)
    bob   = Admin("Bob",   "bob@ex.com",   "abcd", proxy)
    usuarios.extend([alice, bob])

    sala101 = Sala("101")

    r1 = alice.fazer_reserva(sala101, "2025-06-15", "08:00", "10:00", "Matemática")
    alice.modificar_reserva(r1, "2025-06-16", "09:00", "11:00", "Física")

    r2 = bob.criar_reserva_fixa(sala101, "2025-06-20", "14:00", "15:00", "Reunião")

    print("=== Histórico de reservas ===")
    for u in usuarios:
        print(f"- {u.nome} ({u.tipo.value}):")
        for res in u.reservas:
            print("   ", res.to_dict())

if __name__ == "__main__":
    main()
