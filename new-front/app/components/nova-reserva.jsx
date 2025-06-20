import styles from './nova-reserva.module.css'
import { Input, Select, Button } from './form.jsx'

import { add_reserva } from '../lib/api.js'
import { tempo_para_número } from '../lib/tempo.js'

import { useContext } from 'react'
import { FecharReservaModalContext } from './reservaContext.js'

import moment from 'moment'

export default function NovaReserva({ dia, início, fim, lab }) {
  const LABS = ["A03", "A04", "D04", "D05", "D06", "D07"]

  const fecharReserva = useContext(FecharReservaModalContext)

  const handleEnviar = (event) => {
    event.preventDefault() //impede o recarregamento da página
    const form = new FormData(event.target)

    const disp = form.get("disp")
    const prof = form.get("prof")
    const diaInput = form.get("dia")
    const inícioInput = form.get("início")
    const fimInput = form.get("fim")
    const labInput = form.get("lab")

    add_reserva({
      matéria: `${disp} - ${prof}`,
      dia: moment(diaInput).format("YYYY-MM-DD"),
      início: tempo_para_número(inícioInput),                 // hora decimal
      duração: (tempo_para_número(fimInput) - tempo_para_número(inícioInput)) * 60,
      lab: LABS.indexOf(labInput) + 1
    })

    fecharReserva()
  }

  return (
    <form className={styles.grid} onSubmit={handleEnviar}>
      <Input name="prof" desc="Professor" />
      <Input name="disp" desc="Disciplina" />
      <Input name="dia" type="date" desc="Dia" value={dia} />
      <Input name="início" type="time" desc="Início" value={início} />
      <Input name="fim" type="time" desc="Fim" value={fim} />
      <Select name="lab" desc="Laboratório" options={LABS} value={lab} />

      <Button submit desc="Salvar" highlight />
      <Button desc="Cancelar" onClick={fecharReserva} />
    </form>
  )
}
