import { useState, useEffect } from 'react'
import styles from "./visao-diaria.module.css"

import { get_reservas } from '../lib/api.js' 
import Reserva from './reserva.jsx'


export default function VisaoDiaria({ dia, manhã, tarde, noite }) {
  const labs_names = ["A03", "A04", "D04", "D05", "D06", "D07"]

  //Força o formato YYYY-MM-DD
  const data_formatada = typeof dia === "string"
    ? dia
    : new Date(dia).toISOString().slice(0, 10)

  const reservas_data = get_reservas(data_formatada)

  const reservas = reservas_data.map((r, i) => (
    <Reserva
      key={`reserva-${i}`}
      matéria={r.matéria}
      início={r.início}
      duração={r.duração}
      dia={data_formatada}
      lab={r.lab}
      vazia={false}
    />
  ))

  const reservas_manhã = reservas.filter(r => r.props.início <= 12)
  const reservas_tarde = reservas.filter(r => r.props.início > 12 && r.props.início <= 17)
  const reservas_noite = reservas.filter(r => r.props.início > 17)

  const reservas_vazia = []

  for (let lab = 1; lab <= 6; lab++) {
    for (let hour = 8; hour <= 22; hour++) {
      if (
        (hour <= 11 && !manhã) ||
        (hour >= 13 && hour <= 16 && !tarde) ||
        (hour >= 18 && !noite)
      ) continue;

      reservas_vazia.push(
        <Reserva
          key={`vazio-${lab}-${hour}`}
          dia={data_formatada}
          início={hour}
          duração={60}
          lab={lab}
          vazia={true}
          matéria=""
        />
      )
    }
  }

  const filtros = {
    gridTemplateRows: `2rem 
      repeat(${60 * 4}, ${manhã ? "1fr" : "0px"}) 
      repeat(60, 1fr) 
      repeat(${60 * 4}, ${tarde ? "1fr" : "0px"}) 
      repeat(60, 1fr) 
      repeat(${60 * 5}, ${noite ? "1fr" : "0px"})`
  }

  return (
    <div className={styles.reservas} style={filtros}>
      <div className={styles.lab}></div>
      {labs_names.map(lab => (
        <div key={lab} className={styles.lab}>{lab}</div>
      ))}

      {["8h", "9h", "10h", "11h"].map(h =>
        <div key={h} className={styles.hora} style={manhã ? {} : { opacity: 0 }}>{h}</div>
      )}
      <div className={styles.hora}>12h</div>
      {["13h", "14h", "15h", "16h"].map(h =>
        <div key={h} className={styles.hora} style={tarde ? {} : { opacity: 0 }}>{h}</div>
      )}
      <div className={styles.hora}>17h</div>
      {["18h", "19h", "20h", "21h", "22h"].map(h =>
        <div key={h} className={styles.hora} style={noite ? {} : { opacity: 0 }}>{h}</div>
      )}

      {reservas_vazia}
      {manhã ? reservas_manhã : []}
      {tarde ? reservas_tarde : []}
      {noite ? reservas_noite : []}
    </div>
  )
}
