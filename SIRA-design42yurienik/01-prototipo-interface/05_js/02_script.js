// Função para mudar a semana (próxima ou anterior)
function mudarSemana(delta) {
  const semana = document.getElementById("semana-atual");
  let atual = parseInt(semana.dataset.semana || 0);

  // Atualiza a semana com base no delta
  atual += delta;
  semana.dataset.semana = atual;

  // Recupera a data da segunda-feira da semana atual (semana 0)
  const hoje = new Date();
  const segundaBase = new Date(hoje);
  segundaBase.setDate(hoje.getDate() - ((hoje.getDay() + 6) % 7)); // segunda-feira (dia 1)

  // Adiciona (ou subtrai) semanas conforme o número atual
  const novaSegunda = new Date(segundaBase);
  novaSegunda.setDate(segundaBase.getDate() + (atual * 7));

  // Calcula o fim da semana (sexta-feira)
  const novaSexta = new Date(novaSegunda);
  novaSexta.setDate(novaSegunda.getDate() + 4);

  // Atualiza o texto na tela
  semana.textContent = `Semana: ${novaSegunda.toLocaleDateString()} - ${novaSexta.toLocaleDateString()}`;

  // Carrega reservas para a nova semana
  carregarReservas(novaSegunda);
}

// Função para inicializar a semana atual ao carregar a página
function mostrarSemanaAtual() {
  const semana = document.getElementById("semana-atual");
  const hoje = new Date();

  // Calcula segunda-feira da semana atual
  const inicio = new Date(hoje);
  inicio.setDate(hoje.getDate() - ((hoje.getDay() + 6) % 7)); // segunda-feira

  const fim = new Date(inicio);
  fim.setDate(inicio.getDate() + 4); // sexta-feira

  // Exibe o texto da semana
  semana.textContent = `Semana: ${inicio.toLocaleDateString()} - ${fim.toLocaleDateString()}`;
  semana.dataset.semana = 0;

  // Carrega as reservas
  carregarReservas(inicio);
}

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("semana-anterior").addEventListener("click", () => {
    mudarSemana(-1);
  });

  document.getElementById("semana-proximo").addEventListener("click", () => {
    mudarSemana(1);
  });

  mostrarSemanaAtual();
});

// Converte "08h15" ou "08:15" para minutos
function horaParaMinutos(horaStr) {
  const [hora, minuto] = horaStr.replace('h', ':').split(':').map(Number);
  return hora * 60 + (isNaN(minuto) ? 0 : minuto);
}

// Adiciona um bloco visual de reserva
function adicionarReserva(coluna, inicio, fim, turma, materia, professor) {
  const corpo = document.getElementById("corpo-tabela");
  const primeiraLinha = corpo.rows[0];
  const celulaAlvo = primeiraLinha.cells[coluna];

  const minutosInicio = horaParaMinutos(inicio);
  const minutosFim = horaParaMinutos(fim);
  const inicioBase = 8 * 60;
  const minutosDesde8h = minutosInicio - inicioBase;
  const duracaoMin = minutosFim - minutosInicio;

  const alturaHora = primeiraLinha.offsetHeight;
  const topo = (minutosDesde8h / 60) * alturaHora;
  const altura = (duracaoMin / 60) * alturaHora;

  const reserva = document.createElement("div");
  reserva.className = "reserva";
  reserva.style.top = topo + "px";
  reserva.style.height = altura + "px";

  // Abreviações
  const materiaAbrev = materia.split(' ').map(p => p[0]).join('').toUpperCase();
  const professorAbrev = professor.split(' ')[0]; // só o primeiro nome
  const turmaSala = `${turma}`;

  reserva.innerHTML = `
    <div class="resumo-reserva">
      <div class="linha1">${materiaAbrev}</div>
      <div class="linha2">${professorAbrev}</div>
      <div class="linha3">${turmaSala}</div>
    </div>
  `;

  // Tooltip completo no hover
  reserva.title = `${inicio} - ${fim}\n${turma} - ${materia}\n${professor}`;

  celulaAlvo.style.position = "relative";
  celulaAlvo.appendChild(reserva);
}

// Adiciona reserva na semana visível 
function addReservation(date, startTime, endTime, labIndex, turma, materia, professor, semanaAtual) {

  
  const dataReserva = new Date(date);
  dataReserva.setHours(0, 0, 0, 0); // 🔧 Adicionado para corrigir comparações  
  const dataInicioSemana = new Date(semanaAtual);
  dataInicioSemana.setHours(0, 0, 0, 0);
  const dataFimSemana = new Date(dataInicioSemana);
  dataFimSemana.setDate(dataInicioSemana.getDate() + 4);

  if (dataReserva >= dataInicioSemana && dataReserva <= dataFimSemana) {
    const diaSemana = Math.floor((dataReserva - dataInicioSemana) / (1000 * 60 * 60 * 24));

    if (diaSemana < 0 || diaSemana > 4) return;

    const coluna = diaSemana * 6 + labIndex + 1;
    adicionarReserva(coluna, startTime, endTime, turma, materia, professor);
  }
}

// Carrega as reservas para a semana
function carregarReservas(semanaInicio) {
  document.querySelectorAll(".reserva").forEach(div => div.remove()); // Remove reservas anteriores

  const reservas = [
    { date: '2025-04-14', startTime: '08h00', endTime: '10h11', lab: 0, turma: '101', materia: 'Web Design', professor: 'Shirlei' },
    { date: '2025-04-14', startTime: '10h05', endTime: '12h00', lab: 1, turma: '102', materia: 'Lógica de Programação', professor: 'Rodacki' },
    { date: '2025-04-14', startTime: '13h10', endTime: '15h25', lab: 2, turma: '201', materia: 'Banco de Dados', professor: 'Hermano' },
  
    { date: '2025-04-15', startTime: '08h15', endTime: '09h45', lab: 0, turma: '301', materia: 'Programação 2', professor: 'Edwin' },
    { date: '2025-04-15', startTime: '10h10', endTime: '11h55', lab: 1, turma: '202', materia: 'Desenvolvimento de Projeto 1', professor: 'Pizzini' },
    { date: '2025-04-15', startTime: '13h35', endTime: '15h05', lab: 2, turma: '302', materia: 'Desenvolvimento de Projeto 2', professor: 'Uriarte' },
  
    { date: '2025-04-16', startTime: '08h20', endTime: '10h30', lab: 0, turma: '102', materia: 'Lógica de Programação', professor: 'Rodacki' },
    { date: '2025-04-16', startTime: '11h10', endTime: '12h40', lab: 1, turma: '201', materia: 'Banco de Dados', professor: 'Hermano' },
    { date: '2025-04-16', startTime: '18h15', endTime: '20h25', lab: 3, turma: '301', materia: 'Tópicos Avançados em Web', professor: 'Hylson' },
  
    { date: '2025-04-17', startTime: '08h05', endTime: '09h50', lab: 1, turma: '101', materia: 'Web Design', professor: 'Shirlei' },
    { date: '2025-04-17', startTime: '10h30', endTime: '12h00', lab: 2, turma: '302', materia: 'Desenvolvimento de Projeto 2', professor: 'Uriarte' },
    { date: '2025-04-17', startTime: '19h20', endTime: '21h15', lab: 3, turma: '301', materia: 'Programação 2', professor: 'Edwin' },
  
    { date: '2025-04-18', startTime: '08h10', endTime: '09h55', lab: 0, turma: '201', materia: 'Banco de Dados', professor: 'Hermano' },
    { date: '2025-04-18', startTime: '10h25', endTime: '11h40', lab: 1, turma: '202', materia: 'Desenvolvimento de Projeto 1', professor: 'Pizzini' },
    { date: '2025-04-18', startTime: '13h05', endTime: '14h50', lab: 2, turma: '101', materia: 'Web Design', professor: 'Shirlei' },
  
    { date: '2025-04-21', startTime: '15h15', endTime: '17h30', lab: 3, turma: '202', materia: 'Desenv. Projeto 1', professor: 'Pizzini' },
  
    { date: '2025-04-22', startTime: '08h30', endTime: '09h45', lab: 0, turma: '102', materia: 'Lógica de Programação', professor: 'Rodacki' },
    { date: '2025-04-22', startTime: '10h15', endTime: '11h55', lab: 1, turma: '201', materia: 'Banco de Dados', professor: 'Hermano' },
    { date: '2025-04-22', startTime: '18h40', endTime: '20h10', lab: 3, turma: '302', materia: 'Desenvolvimento de Projeto 2', professor: 'Uriarte' },
  
    { date: '2025-04-24', startTime: '11h00', endTime: '11h45', lab: 5, turma: '302', materia: 'Projeto 2', professor: 'Uriarte' },
  
    { date: '2025-04-25', startTime: '09h10', endTime: '10h45', lab: 1, turma: '101', materia: 'Web Design', professor: 'Shirlei' },
    { date: '2025-04-25', startTime: '11h05', endTime: '12h30', lab: 2, turma: '202', materia: 'Desenvolvimento de Projeto 1', professor: 'Pizzini' },
    { date: '2025-04-25', startTime: '13h45', endTime: '15h15', lab: 3, turma: '301', materia: 'Tópicos Avançados em Web', professor: 'Hylson' },
  
    { date: '2025-04-30', startTime: '08h25', endTime: '10h00', lab: 0, turma: '301', materia: 'Programação 2', professor: 'Edwin' },
    { date: '2025-04-30', startTime: '10h20', endTime: '12h05', lab: 2, turma: '102', materia: 'Lógica de Programação', professor: 'Rodacki' },
    { date: '2025-04-30', startTime: '13h10', endTime: '15h00', lab: 3, turma: '201', materia: 'Banco de Dados', professor: 'Hermano' },
  
    { date: '2025-05-06', startTime: '08h45', endTime: '10h15', lab: 0, turma: '301', materia: 'Tópicos Avançados em Web', professor: 'Hylson' },
    { date: '2025-05-06', startTime: '10h30', endTime: '12h20', lab: 1, turma: '302', materia: 'Desenvolvimento de Projeto 2', professor: 'Uriarte' },
    { date: '2025-05-06', startTime: '18h25', endTime: '20h15', lab: 3, turma: '202', materia: 'Desenvolvimento de Projeto 1', professor: 'Pizzini' },
  
    { date: '2025-05-10', startTime: '08h15', endTime: '09h35', lab: 1, turma: '101', materia: 'Web Design', professor: 'Shirlei' },
    { date: '2025-05-10', startTime: '10h00', endTime: '11h45', lab: 2, turma: '201', materia: 'Banco de Dados', professor: 'Hermano' },
    { date: '2025-05-10', startTime: '13h10', endTime: '14h50', lab: 3, turma: '301', materia: 'Programação 2', professor: 'Edwin' },
  
    { date: '2025-05-14', startTime: '08h05', endTime: '09h50', lab: 0, turma: '102', materia: 'Lógica de Programação', professor: 'Rodacki' },
    { date: '2025-05-14', startTime: '10h20', endTime: '11h50', lab: 1, turma: '201', materia: 'Banco de Dados', professor: 'Hermano' },
    { date: '2025-05-14', startTime: '13h25', endTime: '15h00', lab: 2, turma: '302', materia: 'Desenvolvimento de Projeto 2', professor: 'Uriarte' },
  ];
  

  reservas.forEach(reserva => {
    addReservation(reserva.date, reserva.startTime, reserva.endTime, reserva.lab, reserva.turma, reserva.materia, reserva.professor, semanaInicio);
  });
}

// Daqui até a linha 212 é um código para só aparecer os horários da checkboxS
document.addEventListener('DOMContentLoaded', function() {
  const filtros = document.querySelectorAll('.filtro-turno');
  const linhas = document.querySelectorAll('#corpo-tabela tr');

  function atualizarVisibilidade() {
    linhas.forEach(linha => {
      const horaTexto = linha.querySelector('th').textContent.trim();
      const hora = parseInt(horaTexto.replace('h', ''), 10);

      let turno = '';
      if (hora >= 8 && hora <= 12) {
        turno = 'manha';
      } else if (hora >= 13 && hora <= 17) {
        turno = 'tarde';
      } else if (hora >= 18 && hora <= 23) {
        turno = 'noite';
      }

      const checkboxTurno = document.querySelector(`.filtro-turno[value="${turno}"]`);
      if (checkboxTurno && checkboxTurno.checked) {
        linha.style.display = '';
      } else {
        linha.style.display = 'none';
      }
    });
  }

  filtros.forEach(filtro => {
    filtro.addEventListener('change', atualizarVisibilidade);
  });

  atualizarVisibilidade();
});
