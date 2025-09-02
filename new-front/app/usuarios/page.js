"use client";

import { useState } from "react";
import styles from "./usuarios.module.css";
import VisaoDiaria from "./components/visao-diaria.jsx";
import VisaoSemanal from "./components/visao-semanal.jsx";

export default function UsuariosPage() {
  const [logado, setLogado] = useState(false);
  const [mostrarLogin, setMostrarLogin] = useState(false);
  const [usuario, setUsuario] = useState("");
  const [senha, setSenha] = useState("");

  const [visualizacaoSemanal, setVisualizacaoSemanal] = useState(false);

  const efetuarLogin = (e) => {
    e.preventDefault();
    if (usuario === "admin" && senha === "123") {
      setLogado(true);
      setMostrarLogin(false);
      alert("Login realizado com sucesso!");
    } else {
      alert("Usuário ou senha incorretos");
    }
  };

  // Usuários para a tabela
  const [users, setUsers] = useState([
    { id: 1, nome: "Hylson Netto", login: "hvescovi", cadastro: "01/01/2025", email: "hvescovi@gmail.com", status: "Ativado" },
    { id: 2, nome: "Yuri", login: "yuiyui", cadastro: "01/05/2025", email: "yuri@gmail.com", status: "Ativado" },
    { id: 3, nome: "Gustavo Tramontin", login: "gutramon", cadastro: "01/03/2025", email: "gutramon@gmail.com", status: "Bloqueado" },
  ]);

  const [tempStatus, setTempStatus] = useState({});

  const handleStatusChange = (id) => {
    const newStatus = tempStatus[id] || users.find((u) => u.id === id).status;
    setUsers(users.map((user) => (user.id === id ? { ...user, status: newStatus } : user)));
    alert("Status alterado!");
  };

  return (
    <div className={styles.container}>
      {/* Navbar */}
      <header className={styles.headerContainer}>
        <h1 className={styles.logo}>SIRA</h1>
        <nav className={styles.navbar}>
          <ul className={styles.navLinks}>
            <li>
              <button className={styles.linkButton} onClick={() => setVisualizacaoSemanal(false)}>
                Diária
              </button>
            </li>
            <li>
              <button className={styles.linkButton} onClick={() => setVisualizacaoSemanal(true)}>
                Semanal
              </button>
            </li>
            <li>
              <button className={styles.linkButton}>Listagem</button>
            </li>
            <li>
              <button className={styles.linkButton}>Reservar</button>
            </li>
          </ul>
          <div className={styles.navLogin}>
            {!logado ? (
              <button onClick={() => setMostrarLogin(true)}>Login</button>
            ) : (
              <button onClick={() => setLogado(false)}>Logout</button>
            )}
          </div>
        </nav>
      </header>

      {/* Modal Login */}
      {mostrarLogin && (
        <div className={styles.modal}>
          <form className={styles.loginForm} onSubmit={efetuarLogin}>
            <h2>Login</h2>
            <input
              type="text"
              placeholder="Usuário"
              value={usuario}
              onChange={(e) => setUsuario(e.target.value)}
            />
            <input
              type="password"
              placeholder="Senha"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
            />
            <div style={{ marginTop: "1rem", display: "flex", gap: "1rem", justifyContent: "center" }}>
              <button type="submit">Entrar</button>
              <button type="button" onClick={() => setMostrarLogin(false)}>
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Visualização diária ou semanal */}
      {visualizacaoSemanal ? <VisaoSemanal /> : <VisaoDiaria />}

      {/* Tabela de usuários */}
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
                  onChange={(e) => setTempStatus({ ...tempStatus, [user.id]: e.target.value })}
                >
                  {["Ativado", "Bloqueado"].map((status) => (
                    <option key={status} value={status}>
                      {status}
                    </option>
                  ))}
                </select>
                <button className={styles.btnAlterar} onClick={() => handleStatusChange(user.id)}>
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
