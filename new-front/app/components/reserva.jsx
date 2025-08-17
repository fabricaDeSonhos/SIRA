import { Texto } from '../lib/texto.js'
import { hora_para_texto } from '../lib/tempo.js'
import { useContext } from 'react'

import styles from './visao-diaria.module.css'
import { AbrirReservaModalContext } from './reservaContext.js'

export default function Reserva({ id, matéria, dia, início, duração, lab, vazia }) {
  const abrirReserva = useContext(AbrirReservaModalContext)

  const topo = Math.max((início - 8) * 60 + 1, 2)
  const corpo = Texto.limitado(matéria, 40)

  const posicionamento = {
    gridRow: topo,
    gridRowEnd: 'span ' + Math.floor(duração),
    gridColumn: lab + 1,
  }

  const labs_names = ["A03", "A04", "D04", "D05", "D06", "D07"]
  const opts = {
    id,
    dia,
    início: hora_para_texto(início),
    fim: hora_para_texto(início + duração / 60),
    lab: labs_names[lab - 1],
    matéria,
    modoEdicao: !vazia,
  }

  if (vazia) {
    return (
      <div
        className={styles.reserva_vazia}
        style={posicionamento}
        onClick={() => abrirReserva(opts)}
        title={`Clique para reservar ${opts.lab} às ${opts.início}`}
      />
    )
  }

  return (
    <div className={styles.reserva} style={posicionamento}>
      <div>{corpo}</div>
      <div className={styles.acoes}>
        <button
          className={styles.botaoEditar}
          title="Editar reserva"
          onClick={() => abrirReserva(opts)}
        >
          ✏️
        </button>
      </div>
    </div>
  )
}
