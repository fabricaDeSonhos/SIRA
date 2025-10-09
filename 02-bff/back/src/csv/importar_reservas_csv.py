import csv
from datetime import datetime
import os
from src.app import app  # importe sua instância do Flask

from src.config import *
from src.service.common_service import *
from src.service.reservation_service import *

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reservas.csv")

def ler_reservas_csv(caminho_arquivo):
    reservas = []
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                reserva = {
                    "proposito": linha["Propósito"].strip(),
                    "dia": datetime.strptime(linha["dia"], "%Y-%m-%d").date(),
                    "inicio": linha["início"].strip(),
                    "fim": linha["fim"].strip(),
                    "sala": linha["sala"].strip(),
                    "curso": linha["curso"].strip()
                }
                reservas.append(reserva)
                
        return reservas
    except FileNotFoundError:
        print(f"❌ Arquivo '{caminho_arquivo}' não encontrado.")
        return []
    except Exception as e:
        print(f"⚠️ Erro ao ler o arquivo: {e}")
        return []

if __name__ == "__main__":
    with app.app_context():  # <<<<<<<<<< contexto do Flask
        lista_reservas = ler_reservas_csv(CSV_PATH)
        user = get_object_by_id(User, 1)  # usuário fixo para importação

        if lista_reservas:
            print("✅ Reservas importadas com sucesso:\n")
            for r in lista_reservas:
                try:
                    room = get_object_by_name(Room, r['sala'])
                    inicio_hora = datetime.strptime(r['inicio'], "%H:%M").time()
                    fim_hora = datetime.strptime(r['fim'], "%H:%M").time()

                    create_reservation(
                        room, user,
                        purpose=r['proposito'],
                        start_time=inicio_hora,
                        end_time=fim_hora,
                        date=r['dia'],
                        course=r['curso']
                    )

                    print(f"- {r['proposito']} ({r['curso']}) | Sala {r['sala']} | {r['dia']} das {r['inicio']} às {r['fim']}")

                except Exception as e:
                    print(f"⚠️ Erro ao criar reserva: {e}")
