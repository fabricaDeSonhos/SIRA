import styles from './nova-reserva.module.css'

function Entrada({tipo="text", descrição}) {
  return (
    <div id={ descrição } className={styles.entrada}>
      <label htmlFor={ descrição }>{ descrição }</label>
      <input type={tipo} />
    </div>
  )

}

export default function NovaReserva() {
  const LABS = ["A03", "A04", "D04", "D05", "D06", "D07"]
  return (
    <div className={styles.grid}>

    <Entrada descrição="Professor" />
    <Entrada descrição="Disciplina" />
    <Entrada tipo="date" descrição="Dia" />
    <Entrada tipo="time" descrição="Início" />
    <Entrada tipo="time" descrição="Fim" />

    <div className={styles.entrada}>
      <label for="lab">Laboratório</label>
      <select id="lab">
          {LABS.map(l => <option>{l}</option>)}
      </select>
    </div>

     <button className={styles.salvar}>Salvar</button>
     <button className={styles.cancelar}>Cancelar</button>
    </div>
  )

}
