class ModalHandler {
    constructor(openBtnId, closeBtnId, modalId) {
      this.modal = document.getElementById(modalId);
      this.openBtn = document.getElementById(openBtnId);
      this.closeBtn = document.getElementById(closeBtnId);
  
      this.init();
    }
  
    init() {
      if (this.openBtn && this.closeBtn && this.modal) {
        this.openBtn.addEventListener('click', () => this.showModal());
        this.closeBtn.addEventListener('click', () => this.hideModal());
      }
    }
  
    showModal() {
      this.modal.classList.remove('hidden');
    }
  
    hideModal() {
      this.modal.classList.add('hidden');
    }
  }
  
  // Inicialização ao carregar a página
  document.addEventListener('DOMContentLoaded', () => {
    new ModalHandler('openModalBtn', 'closeModalBtn', 'modal');
  });
  