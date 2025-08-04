function reserva(lab, matéria, dia, início, duração) {
  return { lab, matéria, dia, início, duração: duração * 60 }
}

// Mock: reservas fixas (não podem ser removidas via interface)
const hoje = new Date()
const diaHoje = hoje.toISOString().slice(0, 10)
const diaOntem = new Date(hoje.getTime() - 86400000).toISOString().slice(0, 10)

const __reservas = [
  reserva(1, "Projeto Integrador III - 302 Eletro - Prof. Rita", diaHoje, 8, 2.5),
  reserva(1, "INFO 201- Desenvolvimento de Projeto / Prof. Adriano Pizzini", diaHoje, 10.5, 1.5),
  reserva(1, "INFO 202 - Banco de Dados / Prof. Edwin", diaHoje, 13.5, 2.25),
  reserva(1, "Redes (2025) - Turma 2 - Prof. Hewerton", diaHoje, 16, 1.5),

  reserva(1, "MECATRONICA 201 - Lógica de Programação / Prof. Adriano Pizzini", diaOntem, 8, 2.5),
  reserva(1, "ELET. optativas - Desenho assistido por computador / Prof. Cícero", diaOntem, 13.5, 1.5),
  reserva(1, "BCCF01 Algoritmos Hylson Vescovi Netto", diaOntem, 18.5, 1),
  reserva(1, "Pesquisa e Processos Educativos V - Pedagogia - Bernadete e Francini", diaOntem, 19.5, 3.5),

  reserva(2, "MECATRÔNICA 101 / Prof. Cícero", diaHoje, 9.75, 2.25),
  reserva(2, "Elet101 Desenho Técnico Cícero José de Oliveira Lima", diaHoje, 14.25, 1.5),
  reserva(2, "Elet102 Desenho Técnico Cícero José de Oliveira Lima", diaHoje, 15.75, 2.75),

  reserva(2, "BCCF07 Padrões de Projeto / Prof. Ricardo Ladeira", diaOntem, 13.5, 4),
  reserva(2, "BCCF07 Trabalho de Curso I / Prof. Ricardo Ladeira", diaOntem, 18.5, 4.5),
]

// GET reservas: mescla localStorage + mock
export function get_reservas(dia) {
  const dados = localStorage.getItem("reservas")
  const locais = dados ? JSON.parse(dados) : []

  return [...__reservas, ...locais].filter(r => r.dia === dia)
}

// ADD reserva: salva somente no localStorage
export function add_reserva(reserva) {
  const dados = localStorage.getItem("reservas")
  const reservas = dados ? JSON.parse(dados) : []

  reservas.push(reserva)
  localStorage.setItem("reservas", JSON.stringify(reservas))
}

// REMOVE reserva específica (somente do localStorage)
export function remover_reserva({ dia, início, lab }) {
  const dados = localStorage.getItem("reservas")
  if (!dados) return

  const reservas = JSON.parse(dados)

  const novas = reservas.filter(r =>
    !(r.dia === dia && r.início === início && r.lab === lab)
  )

  localStorage.setItem("reservas", JSON.stringify(novas))
}
