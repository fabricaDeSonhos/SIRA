'use client'

import { useState, useEffect } from 'react'
import styles from "./page.module.css"

import {data_bonita} from './lib/tempo.js'
import { Checkbox, Button } from './components/form.jsx'

import VisaoDiaria from "./components/visao-diaria.jsx"
import NovaReserva from "./components/nova-reserva.jsx"
import ReservaInfo from "./components/reserva-info.jsx"
import { AbrirReservaModalContext, FecharReservaModalContext, UserContext } from './components/reservaContext.js'

import {useAuth, useUser} from './lib/api.js'

export default function Home() {
  const [dia, setDia] = useState(new Date())
  const [manhãFiltro, setManhãFiltro] = useState(true)
  const [tardeFiltro, setTardeFiltro] = useState(true)
  const [noiteFiltro, setNoiteFiltro] = useState(true)
  const [reserva, setReserva] = useState(null) // info or edit
  const [toast, setToast] = useState("")

  const [novaReservaOpts, setNovaReservaOpts] = useState({
    dia: "2025-06-07",
    início: "10:30",
    fim: "11:00",
    lab: "A04",
    matéria: "",
    modoEdicao: false
  })

  const auth  = useAuth()
  auth.login("admin", 'admin')

  const user = useUser(auth.loading ? null : auth.token)


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

  const mostrarReservaModal = (type, opt) => {
    setNovaReservaOpts({
      id: opt.id,
      dia: opt.dia,
      início: opt.início,
      fim: opt.fim,
      lab: opt.lab,
      matéria: opt.matéria || "",
      curso: opt.curso,
      modoEdicao: opt.modoEdicao || false
    })
    setReserva(type)
  }

  const fecharReservaModal = (mensagem = "") => {
    setReserva(false)
    if (mensagem) {
      setToast(mensagem)
      setTimeout(() => setToast(""), 3000)
    }
  }

  const handleKeyDown = (e) => {
	  switch (e.key) {
		  case "ArrowRight":
			  inc_dia()
			  break;
		  case "ArrowLeft":
			  dec_dia()
			  break;
		  case "Escape":
			  fecharReservaModal()
			  break
	  }
  }
  useEffect(() => {
	  window.addEventListener('keydown', handleKeyDown)
	  return () => {
		  window.removeEventListener('keydown', handleKeyDown)
	  }
  }, [handleKeyDown])

  return (
    <div className={styles.body} >

      <div className={styles.filtros}>
          <div className={styles.mudança_de_dia}>
            <Button onClick={dec_dia} desc="←" />
            <p><span className={styles.dia_semana}>{data_bonita(dia).dia_semana}, </span> {data_bonita(dia).dia_n} de {data_bonita(dia).mes}</p>
            <Button onClick={inc_dia} desc="→" />
          </div>

        <h1>Visão Diária</h1>
        <div className={styles.filtro}>
          <Checkbox setChecked={setManhãFiltro} checked={manhãFiltro} desc="Manhã" />
          <Checkbox setChecked={setTardeFiltro} checked={tardeFiltro} desc="Tarde" />
          <Checkbox setChecked={setNoiteFiltro} checked={noiteFiltro} desc="Noite" />
        </div>
      </div>

      <AbrirReservaModalContext value={mostrarReservaModal}>
        <FecharReservaModalContext value={fecharReservaModal}>
	  <UserContext value={user.data}>
            <VisaoDiaria
              dia={dia}
              manhã={manhãFiltro}
              tarde={tardeFiltro}
              noite={noiteFiltro}
            />

          <div className={styles.modal}>
            {reserva && reserva === "edit" && <NovaReserva {...novaReservaOpts} />}
            {reserva && reserva === "info" && <ReservaInfo {...novaReservaOpts} />}
          </div>
	  </UserContext>
        </FecharReservaModalContext>
      </AbrirReservaModalContext>

      {/* Toast */}
      {toast && <div className={styles.toast}>{toast}</div>}
    </div>
  )
}
