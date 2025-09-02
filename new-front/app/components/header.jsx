"use client";

import { useState } from "react";
import Link from "next/link";
import styles from "./header.module.css";
import { useLogin } from "./LoginContext";

export default function Header() {
  const { logado, login, logout } = useLogin();
  const [mostrarLogin, setMostrarLogin] = useState(false);
  const [usuario, setUsuario] = useState("");
  const [senha, setSenha] = useState("");

  const efetuarLogin = (e) => {
    e.preventDefault();
    if (login(usuario, senha)) {
      setMostrarLogin(false);
      alert("Login realizado com sucesso!");
    } else {
      alert("Usuário ou senha incorretos");
    }
  };

  return (
    <header className={styles.headerContainer}>
      <h1 className={styles.logo}>SIRA</h1>

      <nav className={styles.navbar}>
        <ul className={styles.navLinks}>
          <li>
            <Link href="/">Diária</Link>
          </li>
          <li>
            <Link href="/visao-semanal">Semanal</Link>
          </li>
          <li>
            <Link href="/listagem">Listagem</Link>
          </li>
          <li>
            <Link href="/reservar">Reservar</Link>
          </li>
          <li>
            <Link href="/admin" className={styles.highlight}>
              Admin
            </Link>
          </li>
          <li>
            <Link href="/primeiro-acesso" className={styles.highlight}>
              Primeiro Acesso
            </Link>
          </li>
        </ul>

        <div className={styles.navLogin}>
          {!logado ? (
            <button onClick={() => setMostrarLogin(true)}>Login</button>
          ) : (
            <button onClick={logout}>Logout</button>
          )}
        </div>
      </nav>

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
              <button type="button" onClick={() => setMostrarLogin(false)}>Cancelar</button>
            </div>
          </form>
        </div>
      )}
    </header>
  );
}
