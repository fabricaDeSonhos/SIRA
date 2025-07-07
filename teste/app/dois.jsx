export default function Coisa_legal() {
  return (
    <div style={{
      backgroundColor: '#f0f0f0',
      padding: '20px',
      borderRadius: '10px',
      textAlign: 'center',
      fontFamily: 'Arial, sans-serif',
      boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
      maxWidth: '300px',
      margin: '50px auto',
      transition: 'transform 0.3s ease, box-shadow 0.3s ease',
      ':hover': {
        transform: 'translateY(-5px)',
        boxShadow: '0 6px 12px rgba(0,0,0,0.15)'
      }
    }}>
      <h2>✨ Coisa Legal ✨</h2>
      <p>Este é um componente simples e bonito feito com React!</p>
      <button style={{
        padding: '10px 15px',
        backgroundColor: '#6200ee',
        color: '#fff',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        transition: 'background-color 0.3s ease, transform 0.2s ease',
        ':hover': {
          backgroundColor: '#7c4dff',
          transform: 'scale(1.05)'
        },
        ':active': {
          transform: 'scale(0.98)'
        }
      }}>
        Clique aqui
      </button>
    </div>
  );
}