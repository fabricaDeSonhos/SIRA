import styles from './nova-reserva.module.css'
import { Input, Select, Button } from './form.jsx'

export default function NovaReserva() {
  const LABS = ["A03", "A04", "D04", "D05", "D06", "D07"]
  return (
    <div className={styles.grid}>

    <Input desc="Professor" />
    <Input desc="Disciplina" />
    <Input type="date" desc="Dia" />
    <Input type="time" desc="Início" />
    <Input type="time" desc="Fim" />

    <Select desc="Laboratório" options={LABS} />

     <Button desc="Salvar" highlight/>
     <Button desc="Cancelar" />
    </div>
  )

}
