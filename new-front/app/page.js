'use client'

import Image from "next/image";
import { useState, useEffect } from 'react'

import styles from "./page.module.css";

import {Checkbox, Button} from './components/form.jsx'

import VisaoDiaria from "./components/visão-diaria.jsx"
import NovaReserva from "./components/nova-reserva.jsx"

import {AbrirReservaModalContext, FecharReservaModalContext} from './components/reservaContext.js'

export default function Home() {
  const [dia, setDia]                 = useState(new Date())
  const [manhãFiltro, setManhãFiltro] = useState(true)
  const [tardeFiltro, setTardeFiltro] = useState(true)
  const [noiteFiltro, setNoiteFiltro] = useState(true)
  const [reserva, setReserva]         = useState(false)

  const [novaReservaOpts, setNovaReservaOpts] = useState({dia:"2025-06-07", início:"10:30", fim:"11:00", lab:"A04"})

  const inc_dia = () => {
    const novoDia = new Date(dia)
    novoDia.setDate(novoDia.getDate() + 1)
    setDia(novoDia)
  }

  const dec_dia = () => {
    const novoDia = new Date(dia)
    novoDia.setDate(novoDia.getDate() - 1)
    setDia(novoDia)
  }

  const mostrarReservaModal = (opt) => {
    const reservaOpts = {
      dia   : opt.dia,
      início: opt.início,
      fim   : opt.fim,
      lab   : opt.lab
    }
    setNovaReservaOpts(reservaOpts)
    setReserva(true)
  }

  const fecharReservaModal = () => setReserva(false)

  // Função para ser passada à grade e permitir clique na área
  const lidarComCliqueNaÁreaBranca = (dadosReserva) => {
    mostrarReservaModal(dadosReserva)
  }

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
          <Checkbox setChecked={setManhãFiltro} checked={manhãFiltro} desc="Manhã"/> 
          <Checkbox setChecked={setTardeFiltro} checked={tardeFiltro} desc="Tarde"/>
          <Checkbox setChecked={setNoiteFiltro} checked={noiteFiltro} desc="Noite"/>
        </div>
      </div>

      <AbrirReservaModalContext value={mostrarReservaModal}>
        <FecharReservaModalContext value={fecharReservaModal}>
          <VisaoDiaria 
            dia={dia}
            manhã={manhãFiltro}
            tarde={tardeFiltro}
            noite={noiteFiltro}
            aoClicarNaÁreaBranca={lidarComCliqueNaÁreaBranca} // <-- Adicionado
          />

          <div className={styles.modal}>
            {reserva && <NovaReserva {...novaReservaOpts} />}
          </div>
        </FecharReservaModalContext>
      </AbrirReservaModalContext>
    </div>
  );
}
