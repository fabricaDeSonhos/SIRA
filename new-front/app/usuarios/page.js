"use client";

import Link from "next/link";
import { useState } from "react";
import styles from "./usuarios.module.css";

export default function UsuariosPage() {
  const [users, setUsers] = useState([
    {
      id: 1,
      nome: "Hylson Netto",
      login: "hvescovi",
      cadastro: "01/01/2025",
      email: "hvescovi@gmail.com",
      status: "Ativado",
    },
    {
      id: 2,
      nome: "Yuri",
      login: "yuiyui",
      cadastro: "01/05/2025",
      email: "yuri@gmail.com",
      status: "Ativado",
    },
    {
      id: 3,
      nome: "Gustavo Tramontin",
      login: "gutramon",
      cadastro: "01/03/2025",
      email: "gutramon@gmail.com",
      status: "Bloqueado",
    },
  ]);

  // Estado temporário para armazenar alterações antes de clicar "Alterar"
  const [tempStatus, setTempStatus] = useState({});

  const handleStatusChange = (id) => {
    const newStatus = tempStatus[id] || users.find((u) => u.id === id).status;
    setUsers(
      users.map((user) =>
        user.id === id ? { ...user, status: newStatus } : user
      )
    );
    alert("Status alterado!");
  };

  return (
    <div className={styles.container}>
      <Link href="/admin" className={styles.returnLink}>
        ← Retornar à página do admin
      </Link>
      <h1 className={styles.titulo}>Configurações de Usuários</h1>

      <table className={styles.userTable}>
        <thead>
          <tr>
            <th>Nome</th>
            <th>Login</th>
            <th>Data de Cadastro</th>
            <th>Email</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.nome}</td>
              <td>{user.login}</td>
              <td>{user.cadastro}</td>
              <td>{user.email}</td>
              <td className={styles.statusCell}>
                <select
                  value={tempStatus[user.id] || user.status}
                  onChange={(e) =>
                    setTempStatus({ ...tempStatus, [user.id]: e.target.value })
                  }
                >
                  <option>Ativado</option>
                  <option>Bloqueado</option>
                </select>
                <button
                  className={styles.btnAlterar}
                  onClick={() => handleStatusChange(user.id)}
                >
                  Alterar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
