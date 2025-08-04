'use client'

import { useState } from 'react'
import VisaoDiaria from './visão-diaria.jsx'
import styles from './visao-diaria.module.css'
import { Button } from './form.jsx'

// Gera os dias úteis (segunda a sábado) da semana baseada no offset
function getWeekDays(baseDate, semanaOffset = 0) {
  const start = new Date(baseDate)
  const mondayOffset = (start.getDay() + 6) % 7
  start.setDate(start.getDate() - mondayOffset + semanaOffset * 7)

  const days = []
  for (let i = 0; i < 6; i++) {
    const d = new Date(start)
    d.setDate(start.getDate() + i)
    days.push(d.toISOString().slice(0, 10))
  }
  return days
}

export default function VisaoSemanal({ manhã = true, tarde = true, noite = true }) {
  const [semanaOffset, setSemanaOffset] = useState(0)
  const hoje = new Date()
  const diasSemana = getWeekDays(hoje, semanaOffset)

  const mudarSemana = (incremento) => {
    setSemanaOffset(semanaOffset + incremento)
  }

  return (
    <div style={{ padding: '1rem' }}>
      {/* Cabeçalho com botões de navegação */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '1rem'
      }}>
        <Button desc="← Semana anterior" onClick={() => mudarSemana(-1)} />
        <h2 style={{ textAlign: 'center', flexGrow: 1 }}>
          Semana de {new Date(diasSemana[0]).toLocaleDateString("pt-BR", { day: '2-digit', month: 'short' })} a {new Date(diasSemana[5]).toLocaleDateString("pt-BR", { day: '2-digit', month: 'short' })}
        </h2>
        <Button desc="Próxima semana →" onClick={() => mudarSemana(1)} />
      </div>

      {/* Grade horizontal com um VisaoDiaria por dia */}
      <div
        style={{
          display: 'flex',
          flexWrap: 'nowrap',
          gap: '2rem',
          overflowX: 'auto',
          paddingBottom: '1rem'
        }}
      >
        {diasSemana.map((dia, index) => (
          <div key={index} style={{ minWidth: '680px' }}>
            <h3 style={{
              textAlign: 'center',
              marginBottom: '0.5rem',
              textTransform: 'capitalize',
              fontSize: '1rem',
              color: '#222'
            }}>
              {new Date(dia).toLocaleDateString("pt-BR", {
                weekday: 'long',
                day: '2-digit',
                month: 'short'
              })}
            </h3>

            <VisaoDiaria
              dia={dia}
              manhã={manhã}
              tarde={tarde}
              noite={noite}
            />
          </div>
        ))}
      </div>
    </div>
  )
}
