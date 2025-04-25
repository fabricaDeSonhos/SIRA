import { exibirLogin } from './modal-login.js';
import { exibirCadastro } from './modal-cadastro.js';
import { exibirEsqueciSenha } from './modal-esqueciSenha.js';

document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("modalLogin");
  const abrirModal = document.getElementById("abrirModalLogin");
  const fecharModal = document.getElementById("fecharModalLogin");
  const semLogin = document.getElementById("linkSemLogin");

  abrirModal.addEventListener("click", () => {
    modal.classList.remove("hidden");
    exibirLogin();
  });

  fecharModal.addEventListener("click", () => {
    modal.classList.add("hidden");
  });

  semLogin.addEventListener("click", () => {
    modal.classList.add("hidden");
  });

  document.getElementById("linkCadastro").addEventListener("click", exibirCadastro);
  document.getElementById("linkEsqueciSenha").addEventListener("click", exibirEsqueciSenha);
  document.getElementById("voltarLogin1").addEventListener("click", exibirLogin);
  document.getElementById("voltarLogin2").addEventListener("click", exibirLogin);
});
