import styles from "./visao-diaria.module.css"

import {useContext} from 'react'
import { useReservations, useUser, useAuth } from '../lib/api.js' 
import {mesmo_dia} from '../lib/tempo.js'
import Reserva from './reserva.jsx'
import {UserContext} from './reservaContext.js'
import { tempo_para_número } from '../lib/tempo.js'


export default function VisaoDiaria({ dia, manhã, tarde, noite, noHours, noText }) {
  const labs_names = ["A03", "A04", "D04", "D05", "D06", "D07"]
//Força o formato YYYY-MM-DD
  const data_formatada = typeof dia === "string"
    ? dia
    : new Date(dia).toISOString().slice(0, 10)

  const {reservations, error, isLoading} = useReservations()
  const user = useContext(UserContext)

  const reservas = isLoading ? [] : reservations.filter(r => mesmo_dia(r.dia, dia)).map((r, i) => (
      <Reserva
        key={r.id}
        id={r.id}
        matéria={r.matéria}
        início={tempo_para_número(r.início)}
        duração={(tempo_para_número(r.fim) - tempo_para_número(r.início)) * 60}
        dia={data_formatada}
        lab={r.lab}
        curso={r.curso}
        vazia={false}
        editavel={user && user.details.id === r.user_id}
        noText={noText}
      />
  ))

  const reservas_manhã = reservas.filter(r => r.props.início <= 12)
  const reservas_tarde = reservas.filter(r => r.props.início > 12 && r.props.início <= 17)
  const reservas_noite = reservas.filter(r => r.props.início > 17)

  const reservas_vazia = []

  for (let lab = 1; lab <= 6; lab++) {
    for (let hour = 8; hour <= 22; hour++) {
      /*if (
        (hour <= 11 && !manhã) ||
        (hour >= 13 && hour <= 16 && !tarde) ||
        (hour >= 18 && !noite)
      ) continue;
      */

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
      repeat(${60 * 5}, ${manhã ? "1fr" : "0fr"}) 
      repeat(${60 * 5}, ${tarde ? "1fr" : "0fr"}) 
      repeat(${60 * 5}, ${noite ? "1fr" : "0fr"})`
  }

  const Horas = [
        ["8", "9", "10", "11", "12"].map(h =>
          <div key={h} className={styles.hora} style={manhã ? {} : { opacity: 0 }}><span className={styles.hora_n}>{h}</span>h</div>
        ),
        ["13", "14", "15", "16","17"].map(h =>
          <div key={h} className={styles.hora} style={tarde ? {} : { opacity: 0 }}><span className={styles.hora_n}>{h}</span>h</div>
        ),
        ["18", "19", "20", "21", "22"].map(h =>
          <div key={h} className={styles.hora} style={noite ? {} : { opacity: 0 }}><span className={styles.hora_n}>{h}</span>h</div>
        ),
        ]
  return (
    <div className={[styles.reservas, noHours ? styles.noHours : ""].join(" ")} style={filtros}>
      <div className={styles.lab}></div>
      {labs_names.map(lab => (
        <div key={lab} className={styles.lab}>{lab}</div>
      ))}

      {!noHours &&
       Horas}

      <div className={styles.lanche_manha}></div>
      <div className={styles.almoco}></div>
      <div className={styles.lanche_tarde}></div>
      <div className={styles.janta}></div>
      <div className={styles.lanche_tarde}></div>
      {reservas_vazia}
      {manhã ? reservas_manhã : []}
      {tarde ? reservas_tarde : []}
      {noite ? reservas_noite : []}


    </div>
  )
}
