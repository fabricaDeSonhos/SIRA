const API_URL = "http://localhost:5000";

// Genérico: tratamento da resposta
async function handleResponse(response) {
  const data = await response.json().catch(() => null);
  return {
    status: response.status,
    data: data,
    ok: response.ok,
    statusText: response.statusText
  };
}

// AUTENTICAÇÃO
export async function register(userData) {
  try {
    const response = await fetch(`${API_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    return await handleResponse(response);
  } catch (error) {
    return { ok: false, error: "Erro de conexão com o servidor" };
  }
}

export async function login(email, password) {
  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    return await handleResponse(response);
  } catch (error) {
    return { ok: false, error: "Erro de conexão com o servidor" };
  }
}

// RESERVA
export async function bookRoom(bookingData) {
  try {
    const token = localStorage.getItem('token');
    if (!token) throw new Error('Usuário não autenticado');

    const response = await fetch(`${API_URL}/bookings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(bookingData)
    });

    return await handleResponse(response);
  } catch (error) {
    return { ok: false, error: error.message || "Erro na reserva" };
  }
}
