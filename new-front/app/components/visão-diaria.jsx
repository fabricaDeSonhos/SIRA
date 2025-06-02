import Image from "next/image";
import { useState, useEffect } from 'react'

import styles from "./visao-diaria.module.css";

import { get_reservas } from '../lib/api.js'
import Reserva from './reserva.jsx'

function texto_limitado(texto, tamanho_máximo) {

    const texto_passou_do_limite = texto && texto.length > tamanho_máximo
    
    if (texto_passou_do_limite) 
      return texto.substr(0,tamanho_máximo-3) + "..."
    return texto
}


export default function VisaoDiaria({dia, manhã, tarde, noite}) {
  const labs_names = ["A03", "A04", "D04", "D05", "D06", "D07"]
  const Labs = labs_names.map(l => <th className={styles.cell}>{ l }</th>)


  const reservas = get_reservas(dia).map(r => <Reserva matéria={r.matéria} início={r.início} duração={r.duração} lab={r.lab} />)
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

      <div className={styles.hora}> 8h</div>
      <div className={styles.hora}> 9h</div>
      <div className={styles.hora}>10h</div>
      <div className={styles.hora}>11h</div>
      <div className={styles.hora}>12h</div>
      <div className={styles.hora}>13h</div>
      <div className={styles.hora}>14h</div>
      <div className={styles.hora}>15h</div>
      <div className={styles.hora}>16h</div>
      <div className={styles.hora}>17h</div>
      <div className={styles.hora}>18h</div>
      <div className={styles.hora}>19h</div>
      <div className={styles.hora}>20h</div>
      <div className={styles.hora}>21h</div>
      <div className={styles.hora}>22h</div>

    {reservas_vazia}
    {manhã ? reservas_manhã : []}
    {tarde ? reservas_tarde : []}
    {noite ? reservas_noite : []}

    </div>
  );
}
