'use client'

import Image from "next/image";
import { useState } from 'react'

import styles from "./page.module.css";

import {Checkbox, Button} from './components/form.jsx'

import VisaoDiaria from "./components/visão-diaria.jsx"
import NovaReserva from "./components/nova-reserva.jsx"


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

  const handleFiltro = e => {}
  return (
    <div>
      <h1>Visualização Diária</h1>
      <div className={styles.filtros}>
        <div className={styles.mudança_de_dia}>
          <Button onClick={dec_dia} desc="-" />
          <p>{dia.toDateString()}</p>
          <Button onClick={inc_dia} desc="+" />
        </div>

        <div className={styles.filtro}>
            <Checkbox setChecked={setManhãFiltro} checked desc="Manhã"/> 
            <Checkbox setChecked={setTardeFiltro} checked desc="Tarde"/>
            <Checkbox setChecked={setNoiteFiltro} checked desc="Noite"/>
        </div>
      </div>


      <VisaoDiaria dia={dia} manhã={manhãFiltro} tarde={tardeFiltro} noite={noiteFiltro}/>


    </div>
  );
}
