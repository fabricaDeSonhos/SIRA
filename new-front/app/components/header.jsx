"use client"; // necessário para hooks do Next.js, se precisar do pathname

import Link from "next/link";
import styles from "./header.module.css";

export default function Header() {
  return (
    <header className={styles.headerContainer}>
      <h1 className={styles.logo}>SIRA</h1>
      <nav className={styles.navbar}>
        <ul>
          <li>
            <Link href="/">Diária</Link>
          </li>
          <li>
            <Link href="/semanal">Semanal</Link>
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
      </nav>
    </header>
  );
}
