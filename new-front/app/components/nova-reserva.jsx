'use client'

import styles from './nova-reserva.module.css'
import { Input, Select, Button } from './form.jsx'

import { add_reserva, remover_reserva } from '../lib/api.js'
import { tempo_para_número } from '../lib/tempo.js'

import { useContext, useState } from 'react'
import { FecharReservaModalContext } from './reservaContext.js'
import {useReservations, useReservation} from '../lib/api.js'

import moment from 'moment'

export default function NovaReserva({id,  dia, início, fim, lab, matéria = "", curso, modoEdicao = false }) {
  const LABS = ["A03", "A04", "D04", "D05", "D06", "D07"]
  const CURSOS = ["bcc","pedagogia","bee","info","eletromecanica","mecatronica","medio"]

  const fecharReserva = useContext(FecharReservaModalContext)


  const {addReserva, deleteReserva, putReserva} = useReservations()

  const [disciplina, professor] = matéria.split(" - ")

  const [emptyPurposeError, setEmptyPurposeError] = useState(false)
  const [negativeDurationError, setNegativeDurationError] = useState(false)
  const [pastDateError, setPastDateError] = useState(false)
  const [smallDurationError, setSmallDurationError] = useState(false)
    
  const clearErrors = () => {
    setEmptyPurposeError(false)
    setNegativeDurationError(false)
    setPastDateError(false)
    setSmallDurationError(false)
  }

  const handleEnviar = (event) => {
    event.preventDefault()
    const form = new FormData(event.target)

    const disp = form.get("disp")
    const diaInput = form.get("dia")
    const inícioInput = form.get("início")
    const fimInput = form.get("fim")
    const labInput = form.get("lab")
    const cursoInput = form.get("curso")

    const novoDia = moment(diaInput).format("YYYY-MM-DD")
    const novoInício = tempo_para_número(inícioInput)
    const novoFim = tempo_para_número(fimInput)
    const novoLab = LABS.indexOf(labInput) + 1

    // ERROR CHECKING
    let someError = false
    if (disp === "") {
      setEmptyPurposeError(true)
      someError = true
    }

    if (novoFim <= novoInício) {
      setNegativeDurationError(true)
      someError = true
    }

    if (moment(diaInput).isBefore(new Date(), 'day')) {
      setPastDateError(true)
      someError = true
    }

    if (novoFim - novoInício < 0.5) {
      setSmallDurationError(true)
      someError = true
    }
    if (someError)
      return


    if (modoEdicao) {

      const reservaObj = {
        start_time: inícioInput + ":00",
        end_time: fimInput + ":00",
        purpose: disp,
        date: diaInput,
        room_id: novoLab,
        course: cursoInput
      }
      putReserva(id, reservaObj) 
    } else {

      addReserva({
        room_id: novoLab,
        date: diaInput,
        start_time: inícioInput + ":00",
        end_time: fimInput + ":00",
        purpose: disp,
        course: cursoInput

      })
    }

    fecharReserva("Reserva salva com sucesso!")
  }

  const handleExcluir = async () => {
    const confirmar = window.confirm("Tem certeza que deseja excluir esta reserva?")
    if (!confirmar) return
    /*
    await remover_reserva({
      dia: moment(dia).format("YYYY-MM-DD"),
      início: tempo_para_número(início),
      lab: LABS.indexOf(lab) + 1,
    })
    */

    deleteReserva(id)
    fecharReserva("Reserva excluída!")
  }


  return (
    <form className={styles.modal} onSubmit={handleEnviar}>
      <h2>{modoEdicao ? "Editar Reserva" : "Nova Reserva"}</h2>

      <div className={styles.content}>
	<Input name="disp" desc="Propósito" value={matéria} error={emptyPurposeError && "Propósitio Vazio"} clearErrors={clearErrors}/>
	<Input name="dia" type="date" desc="Dia" value={dia} error={pastDateError && "Dia está no passado"} clearErrors={clearErrors}/>
	<Input name="início" type="time" desc="Início" value={início} error={negativeDurationError && " Fim ≤ Início"} clearErrors={clearErrors}/>
	<Input name="fim" type="time" desc="Fim" value={fim} error={smallDurationError && "Duração < 30 minutos"} clearErrors={clearErrors}/>
	<Select name="lab" desc="Laboratório" options={LABS} value={lab} />
	<Select name="curso" desc="Curso" options={CURSOS} value={curso} />

      </div>
      <div className={styles.botoes}>
	<Button submit desc={modoEdicao ? "💾 Salvar" : "Reservar"} color="esmeralda"/>
	{modoEdicao && (
	  <Button desc="🗑️ Excluir" onClick={handleExcluir} color="krimson"/>
	)}
	<Button desc="Cancelar" onClick={() => fecharReserva("")} color="preto"/>
      </div>
    </form>
  )
}
