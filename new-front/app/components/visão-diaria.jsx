import styles from "./visao-diaria.module.css"

import { useReservations, useUser } from '../lib/api.js' 
import {mesmo_dia} from '../lib/tempo.js'
import Reserva from './reserva.jsx'


export default function VisaoDiaria({ dia, manhã, tarde, noite, noHours, noText }) {
  const labs_names = ["A03", "A04", "D04", "D05", "D06", "D07"]
//Força o formato YYYY-MM-DD
  const data_formatada = typeof dia === "string"
    ? dia
    : new Date(dia).toISOString().slice(0, 10)

  const {reservations, error, isLoading} = useReservations()
  const user = useUser()

  const dia_das_cores = new Date('2025-09-11T12:12:12')
  console.log(dia_das_cores, dia)
  const exemplo_das_cores = [     
    <Reserva
        key={10}
        id={0}
        matéria={"Computação"}
        início={8}
        duração={60}
        dia={dia_das_cores}
        lab={1}
        vazia={false}

        noText={noText}
        curso="bcc"

      />,
      <Reserva
        key={11}
        id={0}
        matéria={"Pedagogia"}
        início={9}
        duração={60}
        dia={dia_das_cores}
        lab={1}
        vazia={false}

        noText={noText}
        curso="pedagogia"
      />,
      <Reserva
        key={12}
        id={0}
        matéria={"BEE"}
        início={10}
        duração={60}
        dia={dia_das_cores}
        lab={1}
        vazia={false}

        noText={noText}
        curso="bee"
      />,
      <Reserva
        key={13}
        id={0}
        matéria={"Ensino Médio"}
        início={8}
        duração={60}
        dia={dia_das_cores}
        lab={2}
        vazia={false}

        noText={noText}
        curso="medio"
      />,
      <Reserva
        key={14}
        id={0}
        matéria={"Informártica"}
        início={9}
        duração={60}
        dia={dia_das_cores}
        lab={2}
        vazia={false}

        noText={noText}
        curso="info"
      />,
      <Reserva
        key={15}
        id={0}
        matéria={"Eletromecanica"}
        início={10}
        duração={60}
        dia={dia_das_cores}
        lab={2}
        vazia={false}

        noText={noText}
        curso="eletromecanica"
      />,
      <Reserva
        key={16}
        id={0}
        matéria={"Mecatrônica"}
        início={11}
        duração={60}
        dia={dia_das_cores}
        lab={2}
        vazia={false}

        noText={noText}
        curso="mecatronica"
      />,
  ].filter(_ => mesmo_dia(dia, dia_das_cores))

  const reservas = isLoading ? [] : reservations.filter(r => mesmo_dia(r.dia, dia)).map((r, i) => (
    <Reserva
      key={r.id}
      id={r.id}
      matéria={r.matéria}
      início={r.início}
      duração={r.duração}
      dia={data_formatada}
      lab={r.lab}
      vazia={false}

      editavel={!user.isLoading && user.data.details.id === r.user_id} noText={noText}
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

  const Horas = [
        ["8", "9", "10", "11"].map(h =>
          <div key={h} className={styles.hora} style={manhã ? {} : { opacity: 0 }}><span className={styles.hora_n}>{h}</span>h</div>
        ),
        <div className={styles.hora}><span className={styles.hora_n}>12</span>h</div>,
        ["13", "14", "15", "16"].map(h =>
          <div key={h} className={styles.hora} style={tarde ? {} : { opacity: 0 }}><span className={styles.hora_n}>{h}</span>h</div>
        ),
        <div className={styles.hora}><span className={styles.hora_n}>17</span>h</div>,
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



      {exemplo_das_cores}
    </div>
  )
}
