"use client";

import { useState } from "react";
import Link from "next/link";
import styles from "../components/admin.module.css";
import WhitelistTable from "../components/whitelist-table";

export default function AdminPage() {
  const [whitelist, setWhitelist] = useState([
    { id: 1, pattern: "gabriel@gmail.com", permission: "Admin" },
    { id: 2, pattern: "*@ifc.edu.br", permission: "Reservador" },
    { id: 3, pattern: "default", permission: "Visitante" },
  ]);
  const [pattern, setPattern] = useState("");
  const [permission, setPermission] = useState("Visitante");

  const addToWhitelist = () => {
    if (!pattern.trim()) return;
    setWhitelist([...whitelist, { id: Date.now(), pattern, permission }]);
    setPattern("");
  };

  return (
    <div>
      <h2 className={styles.titulo}>Painel Administrativo</h2>
      <div className={styles.card}>
        <h3 className={styles.subtitulo}> Usuários </h3>
        <p className={styles.userCount}>
          {whitelist.length} Usuário{whitelist.length !== 1 && "s"} cadastrado
          {whitelist.length !== 1 && "s"}.
        </p>
        <Link href="/usuarios" className={styles.linkCadastro}>
          Gerenciar Usuários
        </Link>
      </div>

      {/* Tabela */}

      <WhitelistTable whitelist={whitelist} setWhitelist={setWhitelist} />
    </div>
  );
}
