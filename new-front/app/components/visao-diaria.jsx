import styles from "./visao-diaria.module.css"

import { useContext, Fragment } from 'react'
import { useReservations, useUser, useAuth } from '../lib/api.js'
import { mesmo_dia } from '../lib/tempo.js'
import Reserva from './reserva.jsx'
import { UserContext } from './reservaContext.js'
import { tempo_para_número } from '../lib/tempo.js'


export default function VisaoDiaria({ dia, manhã, tarde, noite, salas, noHours, noText }) {
  const labs_names = salas ? Object.values(salas) : []
  const qtd_salas = labs_names.length

  const data_formatada = (dia instanceof Date)
    ? dia.toISOString().slice(0, 10)
    : dia;


  const { reservations, error, isLoading } = useReservations()

  const user = useContext(UserContext)

  const normalizarTempo = (tempo) => {
    if (typeof tempo === 'string') {
      return tempo_para_número(tempo);
    }
    return tempo;
  };

  const reservas = isLoading ? [] : reservations.filter(r => {
    if (!r.dia || !(r.dia instanceof Date)) return false;
    const reserva_data_formatada = r.dia.toISOString().slice(0, 10);
    return reserva_data_formatada === data_formatada;
  }).map((r, i) => {
    const inicioNum = normalizarTempo(r.início);

    const duracao = r.duração

    if (isNaN(duracao) || duracao <= 0) {
      console.error("Reserva com duração inválida:", r);
      return null;
    }
    return (
      <Reserva
        key={r.id}
        id={r.id}
        matéria={r.matéria}
        início={inicioNum}
        duração={duracao}
        dia={data_formatada}
        coluna={salas ? Object.keys(salas).indexOf(r.lab) : 0}
        lab={r.lab}
        curso={r.curso}
        vazia={false}
        editavel={user?.details?.id == r.user_id}
        noText={noText}
      />
    );
  }).filter(Boolean);

  const reservas_manhã = reservas.filter(r => r.props.início <= 12)
  const reservas_tarde = reservas.filter(r => r.props.início > 12 && r.props.início <= 17)
  const reservas_noite = reservas.filter(r => r.props.início > 17)

  const reservas_filtradas = [...(manhã ? reservas_manhã : []), ...(tarde ? reservas_tarde : []), ...(noite ? reservas_noite : [])]


  const reservas_colunas = []
  if (salas) {
    for (let s in Object.keys(salas)) {
      reservas_colunas.push(reservas_filtradas.filter(r => r.props.lab == Object.keys(salas)[s]))
    }
  }

  // insere as reservas vazias
  for (let room = 0; room < qtd_salas; room++) {
    for (let hour = 8; hour <= 22; hour++) {

      if (!reservas_colunas[room])
        reservas_colunas[room] = []

      reservas_colunas[room].push(
        <Reserva
          key={`vazio-${room}-${hour}`}
          dia={data_formatada}
          início={hour}
          duração={60}
          lab={salas ? Object.keys(salas)[room] : ''}
          salas={salas}
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

  const column_styles = {
    gridTemplateColumns: `4rem repeat(${qtd_salas}, 1fr)`
  }
  const coluna_filtros = {
    gridTemplateRows: `
      repeat(${60 * 5}, ${manhã ? "1fr" : "0fr"}) 
      repeat(${60 * 5}, ${tarde ? "1fr" : "0fr"}) 
      repeat(${60 * 5}, ${noite ? "1fr" : "0fr"})`
  }

  const Horas = [
    ["8", "9", "10", "11", "12"].map(h =>
      <div key={h} className={styles.hora} style={manhã ? {} : { opacity: 0 }}><span className={styles.hora_n}>{h}</span>h</div>
    ),
    ["13", "14", "15", "16", "17"].map(h =>
      <div key={h} className={styles.hora} style={tarde ? {} : { opacity: 0 }}><span className={styles.hora_n}>{h}</span>h</div>
    ),
    ["18", "19", "20", "21", "22"].map(h =>
      <div key={h} className={styles.hora} style={noite ? {} : { opacity: 0 }}><span className={styles.hora_n}>{h}</span>h</div>
    ),
  ]
  return (
    <div className={[styles.reservas, noHours ? styles.noHours : ""].join(" ")} style={filtros, column_styles}>
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

      {reservas_colunas.map((c, i) => (

        <div key={`coluna-${i}`} className={styles.coluna} style={{ ...coluna_filtros, gridColumn: i + 2 }}>
          {c.map(reserva => <Fragment key={reserva.key}>{reserva}</Fragment>)}
        </div>
      ))}

      

      

      {/*
      {reservas_vazia}

      {manhã ? reservas_manhã : []}
      {tarde ? reservas_tarde : []}
      {noite ? reservas_noite : []}
      */}


    </div>
  )
}

