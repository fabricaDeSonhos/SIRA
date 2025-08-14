'use client'

import styles from './nova-reserva.module.css'
import { Input, Select, Button } from './form.jsx'

import { add_reserva, remover_reserva } from '../lib/api.js'
import { tempo_para_número } from '../lib/tempo.js'

import { useContext } from 'react'
import { FecharReservaModalContext } from './reservaContext.js'
import moment from 'moment'

export default function NovaReserva({ dia, início, fim, lab, matéria = "", modoEdicao = false }) {
  const LABS = ["A03", "A04", "D04", "D05", "D06", "D07"]
  const fecharReserva = useContext(FecharReservaModalContext)

  const [disciplina, professor] = matéria.split(" - ")

  const handleEnviar = (event) => {
    event.preventDefault()
    const form = new FormData(event.target)

    const disp = form.get("disp")
    const prof = form.get("prof")
    const diaInput = form.get("dia")
    const inícioInput = form.get("início")
    const fimInput = form.get("fim")
    const labInput = form.get("lab")

    const novoDia = moment(diaInput).format("YYYY-MM-DD")
    const novoInício = tempo_para_número(inícioInput)
    const novoFim = tempo_para_número(fimInput)
    const novoLab = LABS.indexOf(labInput) + 1

    if (modoEdicao) {
      remover_reserva({
        dia: moment(dia).format("YYYY-MM-DD"),
        início: tempo_para_número(início),
        lab: LABS.indexOf(lab) + 1,
      })
    }

    add_reserva({
      matéria: `${disp} - ${prof}`,
      dia: novoDia,
      início: novoInício,
      duração: (novoFim - novoInício) * 60,
      lab: novoLab,
    })

    fecharReserva("Reserva salva com sucesso!")
  }

  const handleExcluir = async () => {
    const confirmar = window.confirm("Tem certeza que deseja excluir esta reserva?")
    if (!confirmar) return

    await remover_reserva({
      dia: moment(dia).format("YYYY-MM-DD"),
      início: tempo_para_número(início),
      lab: LABS.indexOf(lab) + 1,
    })

    fecharReserva("Reserva excluída!")
  }


  return (
    <form className={styles.modal} onSubmit={handleEnviar}>
      <h2>{modoEdicao ? "Editar Reserva" : "Nova Reserva"}</h2>

      <Input name="prof" desc="Professor" defaultValue={professor || ""} />
      <Input name="disp" desc="Disciplina" defaultValue={disciplina || ""} />
      <Input name="dia" type="date" desc="Dia" value={dia} />
      <Input name="início" type="time" desc="Início" value={início} />
      <Input name="fim" type="time" desc="Fim" value={fim} />
      <Select name="lab" desc="Laboratório" options={LABS} value={lab} />

      <div className={styles.botoes}>
        <Button submit desc={modoEdicao ? "Salvar Alterações" : "Reservar"} highlight />
        {modoEdicao && (
          <button type="button" className={styles.excluir} onClick={handleExcluir}>
            🗑️ Excluir
          </button>
        )}
        <Button desc="Cancelar" onClick={() => fecharReserva("")} />
      </div>
    </form>
  )
}
