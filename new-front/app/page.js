'use client'

import Image from "next/image";
import styles from "./css/page.module.css";
import VisaoDiaria from "./visão_diaria.js"
import  NovaReserva from "./adicionar_reserva.js"

import { useState } from 'react'

export default function Home() {
  const [dia, setDia]                 = useState(new Date())
  const [manhãFiltro, setManhãFiltro] = useState(true)
  const [tardeFiltro, setTardeFiltro] = useState(true)
  const [noiteFiltro, setNoiteFiltro] = useState(true)

  const inc_dia = () => {
    dia.setDate(dia.getDate() + 1)

    const amanhã = new Date(dia)
    setDia(amanhã)
  }
  const dec_dia = () => {
    dia.setDate(dia.getDate() - 1)
    const ontem = new Date(dia)
    setDia(ontem)
  }

  const flipManhã = () => { setManhãFiltro(!manhãFiltro) }
  const flipTarde = () => { setTardeFiltro(!tardeFiltro) }
  const flipNoite = () => { setNoiteFiltro(!noiteFiltro) }

  const handleFiltro = e => {}
  return (
    <div>
      <h1>Visualização Diária</h1>
      <div className={styles.filtros}>
        <div className={styles.mudança_de_dia}>
          <button onClick={dec_dia}>-</button>
          <p>{dia.toDateString()}</p>
          <button onClick={inc_dia}>+</button>
        </div>

        <div className={styles.filtro}>
            <span><input type="checkbox" checked={manhãFiltro} onChange={flipManhã} /> Manhã</span>
            <span><input type="checkbox" checked={tardeFiltro} onChange={flipTarde} /> Tarde</span>
            <span><input type="checkbox" checked={noiteFiltro} onChange={flipNoite} /> Noite</span>
        </div>
      </div>


      <VisaoDiaria dia={dia} manhã={manhãFiltro} tarde={tardeFiltro} noite={noiteFiltro}/>


    </div>
  );
}
