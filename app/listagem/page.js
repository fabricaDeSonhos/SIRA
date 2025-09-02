"use client";

import React, { useState, useMemo } from "react";
import styles from "./listagem.module.css";


const reservasData = [
  {
    data: "05/04/2025",
    local: "A04",
    horario: "19:00 - 21:00",
    usuario: "hvescovi",
    finalidade: "Ministrar aula de algoritmos",
    turma: "1° fase - superior BCC",
  },
  {
    data: "04/04/2025",
    local: "D05",
    horario: "18:00 - 20:00",
    usuario: "hvescovi",
    finalidade: "Ministrar aula de Introdução à lógica",
    turma: "1° fase - superior BCC",
  },
  {
    data: "03/04/2025",
    local: "A05",
    horario: "20:00 - 22:00",
    usuario: "professorX",
    finalidade: "Utilização de computadores para planilhas",
    turma: "1° fase - técnico informática",
  },
  {
    data: "02/04/2025",
    local: "D04",
    horario: "19:00 - 21:00",
    usuario: "professorY",
    finalidade: "Prova",
    turma: "2º fase - superior BCC",
  },
];

const linhasPorPagina = 10;
const usuarioAtual = "hvescovi";

export default function Listagem() {
  const [paginaAtual, setPaginaAtual] = useState(1);
  const [search, setSearch] = useState("");
  const [minhasReservas, setMinhasReservas] = useState(false);

  const reservasFiltradas = useMemo(() => {
    let filtradas = [...reservasData];

    if (minhasReservas) {
      filtradas = filtradas.filter((r) => r.usuario === usuarioAtual);
    }

    if (search.trim() !== "") {
      filtradas = filtradas.filter((r) =>
        Object.values(r).some((valor) =>
          valor.toLowerCase().includes(search.toLowerCase())
        )
      );
    }

    return filtradas;
  }, [search, minhasReservas]);

  const totalPaginas = Math.ceil(reservasFiltradas.length / linhasPorPagina);
  const reservasPagina = reservasFiltradas.slice(
    (paginaAtual - 1) * linhasPorPagina,
    paginaAtual * linhasPorPagina
  );

  const mudarPagina = (pagina) => setPaginaAtual(pagina);

  return (
    <div className={styles.container}>
      <h2 className={styles.titulo}>Histórico de Reservas</h2>

      <div className={styles.filtros}>
        <input
          type="text"
          placeholder="Pesquisar..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className={styles.searchInput}
        />
        <label className={styles.checkboxLabel}>
          <input
            type="checkbox"
            checked={minhasReservas}
            onChange={(e) => setMinhasReservas(e.target.checked)}
          />
          Minhas Reservas
        </label>
      </div>

      <table className={styles.tabela}>
        <thead>
          <tr>
            <th>Data</th>
            <th>Local</th>
            <th>Horário</th>
            <th>Usuário</th>
            <th>Finalidade</th>
            <th>Turma</th>
          </tr>
        </thead>
        <tbody>
          {reservasPagina.map((reserva, idx) => (
            <tr key={idx}>
              <td>{reserva.data}</td>
              <td>{reserva.local}</td>
              <td>{reserva.horario}</td>
              <td>
                <strong>{reserva.usuario}</strong>
              </td>
              <td>
                <em>{reserva.finalidade}</em>
              </td>
              <td>{reserva.turma}</td>
            </tr>
          ))}
          {reservasPagina.length === 0 && (
            <tr>
              <td colSpan="6" className={styles.semReservas}>
                Nenhuma reserva encontrada.
              </td>
            </tr>
          )}
        </tbody>
      </table>

      <div className={styles.pagination}>
        {Array.from({ length: totalPaginas }, (_, i) => (
          <button
            key={i + 1}
            onClick={() => mudarPagina(i + 1)}
            className={paginaAtual === i + 1 ? styles.active : ""}
          >
            {i + 1}
          </button>
        ))}
      </div>
    </div>
  );
}
