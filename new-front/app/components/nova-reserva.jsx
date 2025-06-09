import styles from './nova-reserva.module.css'
import { Input, Select, Button } from './form.jsx'

import {new_reserva} from '../lib/api.js'
import { tempo_para_número } from '../lib/tempo.js'

import { useContext } from 'react'
import { FecharReservaModalContext } from './reservaContext.js'

import moment from 'moment'

export default function NovaReserva({dia, início, fim, lab}) {
  const LABS = ["A03", "A04", "D04", "D05", "D06", "D07"]

  const fecharReserva = useContext(FecharReservaModalContext)


  const handleEnviar = (form) => {
    const disp   = form.get("disp")
    const prof   = form.get("prof")
    const dia    = form.get("dia")
    const início = form.get("início")
    const fim    = form.get("fim")
    const lab    = form.get("lab")


    const labs_names = ["A03", "A04", "D04", "D05", "D06", "D07"]
    new_reserva(
      labs_names.indexOf(lab)+1,
      disp + " - " + prof,
      moment(dia).date(), 
      tempo_para_número(início), 
      tempo_para_número(fim) - tempo_para_número(início)
    )
    fecharReserva()
  }
  return (
    <form className={styles.grid} action={handleEnviar}>

    <Input name="prof" desc="Professor" />
    <Input name="disp" desc="Disciplina" />
    <Input name="dia" type="date" desc="Dia" value={dia}/>
    <Input name="início" type="time" desc="Início" value={início}/>
    <Input name="fim" type="time" desc="Fim" value={fim}/>

    <Select name="lab" desc="Laboratório" options={LABS} value={lab}/>

    <Button submit desc="Salvar" highlight />
    <Button desc="Cancelar" onClick={fecharReserva}/>
    </form>
  )

}
