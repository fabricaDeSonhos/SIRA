import styles from './nova-reserva.module.css'
import { Input, Select, Button } from './form.jsx'

import { useContext } from 'react'
import { FecharReservaModalContext } from './reservaContext.js'

export default function NovaReserva({dia, início, fim, lab}) {
  const LABS = ["A03", "A04", "D04", "D05", "D06", "D07"]

  const fecharReserva = useContext(FecharReservaModalContext)

  return (
    <div className={styles.grid}>

    <Input desc="Professor" />
    <Input desc="Disciplina" />
    <Input type="date" desc="Dia" value={dia}/>
    <Input type="time" desc="Início" value={início}/>
    <Input type="time" desc="Fim" value={fim}/>

    <Select desc="Laboratório" options={LABS} value={lab}/>

     <Button desc="Salvar" highlight onClick={fecharReserva}/>
     <Button desc="Cancelar" onClick={fecharReserva}/>
    </div>
  )

}
