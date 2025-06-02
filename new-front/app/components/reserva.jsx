import { Texto } from '../lib/texto.js'
import styles from './visao-diaria.module.css'

export default function Reserva({matéria, início, duração, lab, vazia}) {

    const topo = Math.max((início - 8)*60 + 1, 2)

    const corpo = Texto.limitado(matéria, 40)

  const posicionamento = {
    gridRow: topo,
    gridRowEnd: 'span ' + duração,
    gridColumn: lab+1
  }

    if (vazia)
      return  <div className={styles.reserva_vazia} style={posicionamento}></div>
    return (

      <div title={matéria} className={styles.reserva} style={posicionamento}>
        {corpo}
      </div>
  )
}
