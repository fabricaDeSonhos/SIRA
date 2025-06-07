import { Texto } from '../lib/texto.js'
import { hora_para_texto } from '../lib/tempo.js'

import { Button } from './form.jsx'

import { useContext } from 'react'

import styles from './visao-diaria.module.css'

import { AbrirReservaModalContext } from './reservaContext.js'

export default function Reserva({matéria, dia, início, duração, lab, vazia}) {

    const abrirReserva = useContext(AbrirReservaModalContext)

    const topo = Math.max((início - 8)*60 + 1, 2)

    const corpo = Texto.limitado(matéria, 40)

  const posicionamento = {
    gridRow: topo,
    gridRowEnd: 'span ' + duração,
    gridColumn: lab+1
  }

  const labs_names = ["A03", "A04", "D04", "D05", "D06", "D07"]
  const opts = {
    dia: dia,
    início: hora_para_texto(início),
    fim: hora_para_texto(início+(duração/60)),
    lab: labs_names[lab-1]
  }

    if (vazia)
      return  <div className={styles.reserva_vazia} style={posicionamento}>
      <Button desc="+" onClick={() => abrirReserva(opts)}/>
    </div>
    return (

      <div title={matéria} className={styles.reserva} style={posicionamento}>
        {corpo}
      </div>
  )
}
