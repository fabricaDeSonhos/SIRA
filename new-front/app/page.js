'use client'

import { useState } from 'react'
import styles from "./page.module.css"

import { Checkbox, Button } from './components/form.jsx'

import VisaoDiaria from "./components/visão-diaria.jsx"
import VisaoSemanal from "./components/visao-semanal.jsx"
import NovaReserva from "./components/nova-reserva.jsx"

import { AbrirReservaModalContext, FecharReservaModalContext } from './components/reservaContext.js'

export default function Home() {
  const [dia, setDia] = useState(new Date())
  const [manhãFiltro, setManhãFiltro] = useState(true)
  const [tardeFiltro, setTardeFiltro] = useState(true)
  const [noiteFiltro, setNoiteFiltro] = useState(true)
  const [reserva, setReserva] = useState(false)
  const [toast, setToast] = useState("")
  const [visualizacaoSemanal, setVisualizacaoSemanal] = useState(false)

  const [novaReservaOpts, setNovaReservaOpts] = useState({
    dia: "2025-06-07",
    início: "10:30",
    fim: "11:00",
    lab: "A04",
    matéria: "",
    modoEdicao: false
  })

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
    setNovaReservaOpts({
      id: opt.id,
      dia: opt.dia,
      início: opt.início,
      fim: opt.fim,
      lab: opt.lab,
      matéria: opt.matéria || "",
      modoEdicao: opt.modoEdicao || false
    })
    setReserva(true)
  }

  const fecharReservaModal = (mensagem = "") => {
    setReserva(false)
    if (mensagem) {
      setToast(mensagem)
      setTimeout(() => setToast(""), 3000)
    }
  }

  const lidarComCliqueNaÁreaBranca = (dadosReserva) => {
    mostrarReservaModal(dadosReserva)
  }

  const abrirReservaVaziaManual = () => {
    const hoje = new Date().toISOString().slice(0, 10)
    mostrarReservaModal({
      dia: hoje,
      início: "08:00",
      fim: "09:00",
      lab: "A03",
      matéria: "",
      modoEdicao: false
    })
  }

  return (
    <div>
      <h1>{visualizacaoSemanal ? "Visualização Semanal" : "Visualização Diária"}</h1>

      <div className={styles.filtros}>
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
            <input
              type="checkbox"
              checked={visualizacaoSemanal}
              onChange={() => setVisualizacaoSemanal(!visualizacaoSemanal)}
            />
            Visualização semanal
          </label>
        </div>

        {!visualizacaoSemanal && (
          <div className={styles.mudança_de_dia}>
            <Button onClick={dec_dia} desc="←" />
            <p>{dia.toDateString()}</p>
            <Button onClick={inc_dia} desc="→" />
          </div>
        )}

        <div className={styles.filtro}>
          <Checkbox setChecked={setManhãFiltro} checked={manhãFiltro} desc="Manhã" />
          <Checkbox setChecked={setTardeFiltro} checked={tardeFiltro} desc="Tarde" />
          <Checkbox setChecked={setNoiteFiltro} checked={noiteFiltro} desc="Noite" />
        </div>
      </div>

      <AbrirReservaModalContext value={mostrarReservaModal}>
        <FecharReservaModalContext value={fecharReservaModal}>
          {visualizacaoSemanal ? (
            <VisaoSemanal manhã={manhãFiltro} tarde={tardeFiltro} noite={noiteFiltro} />
          ) : (
            <VisaoDiaria
              dia={dia}
              manhã={manhãFiltro}
              tarde={tardeFiltro}
              noite={noiteFiltro}
              aoClicarNaÁreaBranca={lidarComCliqueNaÁreaBranca}
            />
          )}

          {/* Botão flutuante */}
          <button className={styles.fab} onClick={abrirReservaVaziaManual} title="Nova Reserva Manual">
            ➕
          </button>

          {/* Modal */}
          <div className={styles.modal}>
            {reserva && <NovaReserva {...novaReservaOpts} />}
          </div>
        </FecharReservaModalContext>
      </AbrirReservaModalContext>

      {/* Toast */}
      {toast && <div className={styles.toast}>{toast}</div>}
    </div>
  )
}
