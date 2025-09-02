"use client";

import { useState } from "react";
import Swal from "sweetalert2";
import styles from "./admin.module.css";

export default function WhitelistTable() {
  const [whitelist, setWhitelist] = useState([
    { id: 1, pattern: "gabriel@gmail.com", permission: "Admin" },
    { id: 2, pattern: "*@ifc.edu.br", permission: "Reservador" },
    { id: 3, pattern: "default", permission: "Visitante" },
  ]);

  const [pattern, setPattern] = useState("");
  const [permission, setPermission] = useState("Visitante");

  // Função para adicionar à whitelist
  const addToWhitelist = () => {
    if (!pattern.trim()) return;
    setWhitelist([...whitelist, { id: Date.now(), pattern, permission }]);
    setPattern("");
  };

  // Função para deletar
  const confirmDelete = (id) => {
    Swal.fire({
      title: "Tem certeza?",
      text: "Você quer excluir esta permissão?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#3085d6",
      confirmButtonText: "Sim, excluir!",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        setWhitelist(whitelist.filter((item) => item.id !== id));
        Swal.fire("Excluído!", "A permissão foi removida.", "success");
      }
    });
  };

  const permissionClass = (perm) => {
    if (perm === "Admin") return styles.permissionAdmin;
    if (perm === "Reservador") return styles.permissionReservador;
    return styles.permissionVisitante;
  };

  return (
    <div>
      <h2 className={styles.subtituloTabela}>Gerenciar Whitelist</h2>
      <div className={styles.cardTabela}>
        {/* Formulário */}
        <div className={styles.formRow}>
          <input
            className={styles.input}
            type="text"
            placeholder="Expressão..."
            value={pattern}
            onChange={(e) => setPattern(e.target.value)}
          />
          <select
            className={styles.select}
            value={permission}
            onChange={(e) => setPermission(e.target.value)}
          >
            <option value="Visitante">Visitante</option>
            <option value="Reservador">Reservador</option>
            <option value="Admin">Admin</option>
          </select>
          <button className={styles.addBtn} onClick={addToWhitelist}>
            +
          </button>
        </div>

        {/* Tabela */}
        <div className={styles.tableContainer}>
          <table className={styles.table}>
            <thead className={styles.tableHeader}>
              <tr>
                <th>Expressão</th>
                <th>Permissão</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              {whitelist.map((item) => (
                <tr key={item.id}>
                  <td className={styles.textCinza}>{item.pattern}</td>
                  <td className={permissionClass(item.permission)}>
                    {item.permission}
                  </td>
                  <td>
                    <button
                      className={styles.deleteBtn}
                      onClick={() => confirmDelete(item.id)}
                    >
                      X
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
