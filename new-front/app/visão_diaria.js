import Image from "next/image";
import styles from "./css/visao_diaria.module.css";
import { __reservas } from './utils.js'
import { useState } from 'react'

function Reserva({matéria, início, duração, lab, vazia}) {

    const topo = (início - 8)*60 + 1

    const MAX_LEN = 40
    const texto_grande = matéria && matéria.length > MAX_LEN
    const corpo =  texto_grande ? matéria.substr(1,MAX_LEN-3) + "..." : matéria

    const estilos = {
      gridColumn: lab+1,
      gridRow: (topo == 1 ? 2 : topo) + " / span "  + duração,
    }

    if (vazia)
      return  <div className={styles.reserva_vazia} style={estilos}></div>
    return (
    <div title={matéria} className={styles.reserva} style={estilos}>
      {corpo}
    </div>
  )
}

function get_reservas(dia) {
  const hoje = (new Date()).getDate()

  return __reservas
    .filter(r => r.dia == dia.getDate())
    .map(r => <Reserva matéria={r.matéria} início={r.início} duração={r.duração} lab={r.lab} />)

}

export default function VisaoDiaria({dia, manhã, tarde, noite}) {
  const labs_names = ["A03", "A04", "D04", "D05", "D06", "D07"]
  const Labs = labs_names.map(l => <th className={styles.cell}>{ l }</th>)


  const reservas = get_reservas(dia)
  const reservas_manhã = reservas.filter( r => r.props.início <= 12)
  const reservas_tarde = reservas.filter( r => r.props.início > 12 && r.props.início <= 17)
  const reservas_noite = reservas.filter( r => r.props.início > 17)

  let reservas_vazia = []

  for (let lab=1; lab<=6; lab++) {
    for (let hour=8; hour<= 22; hour++) {
      reservas_vazia.push(<Reserva início={hour} duração={60} lab={lab} vazia />)
    }

  }
  return (
    <div className={styles.reservas}>
      <div className={styles.lab}>   </div>
      <div className={styles.lab}>A03</div>
      <div className={styles.lab}>A04</div>
      <div className={styles.lab}>D04</div>
      <div className={styles.lab}>D05</div>
      <div className={styles.lab}>D06</div>
      <div className={styles.lab}>D07</div>

      <div className={styles.hora} style={{ gridRow: 1 +  1     + '/ span 60' }}> 8h</div>
      <div className={styles.hora} style={{ gridRow: 1 +  1*60  + '/ span 60' }}> 9h</div>
      <div className={styles.hora} style={{ gridRow: 1 +  2*60  + '/ span 60' }}>10h</div>
      <div className={styles.hora} style={{ gridRow: 1 +  3*60  + '/ span 60' }}>11h</div>
      <div className={styles.hora} style={{ gridRow: 1 +  4*60  + '/ span 60' }}>12h</div>
      <div className={styles.hora} style={{ gridRow: 1 +  5*60  + '/ span 60' }}>13h</div>
      <div className={styles.hora} style={{ gridRow: 1 +  6*60  + '/ span 60' }}>14h</div>
      <div className={styles.hora} style={{ gridRow: 1 +  7*60  + '/ span 60' }}>15h</div>
      <div className={styles.hora} style={{ gridRow: 1 +  8*60  + '/ span 60' }}>16h</div>
      <div className={styles.hora} style={{ gridRow: 1 +  9*60  + '/ span 60' }}>17h</div>
      <div className={styles.hora} style={{ gridRow: 1 + 10*60  + '/ span 60' }}>18h</div>
      <div className={styles.hora} style={{ gridRow: 1 + 11*60  + '/ span 60' }}>19h</div>
      <div className={styles.hora} style={{ gridRow: 1 + 12*60  + '/ span 60' }}>20h</div>
      <div className={styles.hora} style={{ gridRow: 1 + 13*60  + '/ span 60' }}>21h</div>
      <div className={styles.hora} style={{ gridRow: 1 + 14*60  + '/ span 60' }}>22h</div>

    {reservas_vazia}
    {manhã ? reservas_manhã : []}
    {tarde ? reservas_tarde : []}
    {noite ? reservas_noite : []}

    </div>
  );
}
