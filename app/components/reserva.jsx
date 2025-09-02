// Reserva.jsx
"use client";

import { useState, useEffect, useContext } from "react";
import { Texto } from "../lib/texto.js";
import { hora_para_texto } from "../lib/tempo.js";
import styles from "./visao-diaria.module.css";
import { AbrirReservaModalContext, FecharReservaModalContext } from "./reservaContext.js";

export default function Reserva({ matéria, dia, início, duração, lab, vazia }) {
  const abrirReserva = useContext(AbrirReservaModalContext);

  const [posicionamento, setPosicionamento] = useState({ gridRow: 0, gridRowEnd: 0, gridColumn: 0 });
  const [corpo, setCorpo] = useState("");

  useEffect(() => {
    setCorpo(Texto.limitado(matéria, 40));
    const topoCalc = Math.max((início - 8) * 60 + 1, 2);
    setPosicionamento({
      gridRow: topoCalc,
      gridRowEnd: 'span ' + duração,
      gridColumn: lab + 1,
    });
  }, [matéria, início, duração, lab]);

  const labs_names = ["A03", "A04", "D04", "D05", "D06", "D07"];
  const opts = {
    dia,
    início: hora_para_texto(início),
    fim: hora_para_texto(início + duração / 60),
    lab: labs_names[lab - 1],
    matéria,
    modoEdicao: !vazia,
  };

  if (vazia) {
    return (
      <div
        className={styles.reserva_vazia}
        style={posicionamento}
        onClick={() => abrirReserva(opts)}
        title={`Clique para reservar ${opts.lab} às ${opts.início}`}
      />
    );
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
  );
}
