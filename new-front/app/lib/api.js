
function reserva(lab, matéria, dia, início, duração) {
    return {lab, matéria, dia, início, duração: duração*60}
}

const hoje = (new Date()).getDate()

const __reservas = [
  reserva(1, "Projeto Integrador III - 302 Eletro - Prof. Rita", hoje, 8, 2.5)
 ,reserva(1, "INFO 201- Desenvolvimento de Projeto / Prof. Adriano Pizzini", hoje, 10.5, 1.5)
 ,reserva(1, "INFO 202 - Banco de Dados / Prof. Edwin", hoje, 13.5, 2.25)
 ,reserva(1, "Redes (2025) - Turma 2 - Prof. Hewerton", hoje, 16, 1.5)

  ,reserva(1, "MECATRONICA 201 - Lógica de Programação / Prof. Adriano Pizzini", hoje-1, 8, 2.5)
  ,reserva(1, "ELET. optativas - Desenho assistido por computador / Prof. Cícero", hoje-1, 13.5, 1.5)
  ,reserva(1, "BCCF01 Algoritmos Hylson Vescovi Netto", hoje-1, 18.5, 1)
  ,reserva(1, " Pesquisa e Processos Educativos V - Turma 2023 - Pedagogia (5ª fase) - Professoras Bernadete e Francini", hoje-1, 19.5, 3.5)


  ,reserva(2, "MECATRÔNICA 101 / Prof. Cícero", hoje, 9.75, 2.25)
  ,reserva(2, "Elet101 Desenho Técnico Cícero José de Oliveira Lima", hoje, 14.25,1.5)
  ,reserva(2, "Elet102 Desenho Técnico Cícero José de Oliveira Lima", hoje, 15.75, 2.75)

  ,reserva(2, "BCCF07 Padrões de Projeto / Prof. Ricardo Ladeira", hoje-1, 13.5, 4)
  ,reserva(2, "BCCF07 Trabalho de Curso I / Prof. Ricardo Ladeira", hoje-1, 18.5, 4.5)
]

export function get_reservas(dia) {
  const hoje = (new Date()).getDate()

  return __reservas
    .filter(r => r.dia == dia.getDate())

}

export function new_reserva(lab, matéria, dia, início, duração) {
    __reservas.push(reserva(lab, matéria, dia, início, duração))
}
