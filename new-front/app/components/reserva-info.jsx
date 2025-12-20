'use client'

import styles from './nova-reserva.module.css'
import { Input, Select, Button } from './form.jsx'

import { add_reserva, remover_reserva } from '../lib/api.js'
import { tempo_para_número } from '../lib/tempo.js'

import { useContext, useState } from 'react'
import { FecharReservaModalContext } from './reservaContext.js'
import {useReservations, useReservation} from '../lib/api.js'

import moment from 'moment'

export default function ReservaInfo({id, dia, início, fim, lab, matéria = "", curso }) {
  const LABS = ["A03", "A04", "D04", "D05", "D06", "D07"]
  const CURSOS = ["bcc","pedagogia","bee","info","eletromecanica","mecatronica","medio"]

  const fecharReserva = useContext(FecharReservaModalContext)

  return (
    <div className={styles.modal} >
      <h2>Sobre</h2>
      <div className={styles.content}>
	<p><strong>Propósito: </strong>{matéria}</p>
	<p><strong>Dia: </strong>{dia}</p>
	<p><strong>Início: </strong>{início}</p>
	<p><strong>Fim: </strong>{fim}</p>
	<p><strong>Sala: </strong>{lab}</p>
	<p><strong>Curso: </strong>{curso}</p>
      </div>

      <div className={styles.botoes}>
        <Button desc="Fechar" onClick={() => fecharReserva("")} color="preto"/>
      </div>
    </div>
  )
}
