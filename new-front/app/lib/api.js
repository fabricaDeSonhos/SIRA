import useSWR from 'swr';
import {useState, useEffect} from 'react'
import {tempo_para_número} from './tempo.js'


const API_BASE_URL = !process.env.NEXT_PUBLIC_API ? "http://localhost:5000" : process.env.NEXT_PUBLIC_API

function update_obj(source, changes) {
  for (let key in changes) {
    if (key in source)
      source[key] = changes[key]
  }
}

export const fetcher = async (url) => {
  const res = await fetch(`${API_BASE_URL}${url}`);
  if (!res.ok) {
    const error = new Error("An error occurred while fetching the data.");
    error.status = res.status;
    throw error;
  }
  return res.json();

};
export const fetcher_jwt = async (url, token) => {
  const res = await fetch(`${API__BASE_URL}${url}`, {
    headers: {
      'Authorization': 'Bearer ' + token
    }
  });
  if (!res.ok) {
    const error = new Error("An error occurred while fetching the data.");
    error.status = res.status;
    throw error;
  }
  return res.json();

};

function api2reserva(api_res) {
  const hoje = new Date()
  const diaHoje = hoje.toISOString().slice(0, 10)

  const id = api_res.id
  const lab = api_res.room_id
  const matéria = api_res.purpose
  const dia = new Date(api_res.date + "T12:00:00") // without adding T12:00:00 it defaults to midnight, and because of Brazil's timezone, it goes a day earlier
  const início = tempo_para_número(api_res.start_time)
  const duração = tempo_para_número(api_res.end_time) - início
  const user_id= api_res.user_id
  const curso = api_res.course

  return {id, user_id, lab, matéria, curso, dia, início, duração: duração*60}
}


const _useReservations = (token, logout) => {
  // A busca por reservas só ocorre se houver um token
  const { data, error, isLoading, mutate } = useSWR(token ? '/reservations' : null, fetcher, {refreshInterval: 1000});
  
  // Função centralizada para tratar erros de autenticação
  const handleAuthError = (e) => {
      if (e.message && e.message.includes("Token has expired")) {
          console.error("Sessão expirada. Fazendo logout.");
          if(logout) logout();
      } else {
          // Não relança o erro de conflito, pois ele já foi tratado
          if (!e.message || !e.message.includes("Conflict")) {
            console.error("Ocorreu um erro na operação:", e);
          }
      }
  }

  const addReserva = async (newItem) => {
    if (!token) return;
    try {
      const req = await fetch(`${API_BASE_URL}/reservations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(newItem),
      });

      if (!req.ok) {
        if (req.status === 401) throw new Error("Token has expired");
        if (req.status === 409) throw new Error("Conflict"); // Erro específico para conflito
        const errorBody = await req.text();
        throw new Error(`Falha ao adicionar a reserva: ${errorBody}`);
      }
      
      // Ao criar com sucesso, revalida os dados do servidor e AGUARDA a conclusão.
      // Isso garante que a UI terá os dados mais recentes antes de continuar.
      await mutate();

    } catch (e) {
      handleAuthError(e);
      throw e; // Relança o erro para o componente poder capturá-lo
    }
  };

  const deleteReserva = async (reservaId) => {
      if (!token) return;
      const optimisticData = data
      optimisticData.details = data.details.filter((u) => u.id !== reservaId);
      mutate(optimisticData, false);

      try {
        const req = await fetch(`${API_BASE_URL}/reservations/${reservaId}`, {
          method: 'DELETE',
          headers: { "Authorization": 'Bearer ' + token }
        });

        if (!req.ok) {
            if (req.status === 401) throw new Error("Token has expired");
            const errorBody = await req.text();
            throw new Error(`Falha ao excluir a reserva: ${errorBody}`);
        }
        await mutate(); // Revalida após a exclusão
      } catch (error) {
        handleAuthError(error);
        mutate(data); // Reverte a UI em caso de erro
      }
    };

  const putReserva = async (reservaId, changesObj) => {
    if (!token) return;
    
    // Atualização otimista da UI para resposta rápida
    const optimisticData = JSON.parse(JSON.stringify(data));
    const reservationIndex = optimisticData.details.findIndex(x => x.id == reservaId)
    if(reservationIndex > -1){
        update_obj(optimisticData.details[reservationIndex], changesObj)
    }
    mutate(optimisticData, false)

    try {
      const req = await fetch(`${API_BASE_URL}/reservations/${reservaId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token 
        },
        body: JSON.stringify(changesObj)
      })
      if (!req.ok) {
            if (req.status === 401) throw new Error("Token has expired");
            if (req.status === 409) throw new Error("Conflict");
            const errorBody = await req.text();
            throw new Error(`Falha ao editar a reserva: ${errorBody}`);
      }
      // Revalida os dados e aguarda a conclusão
      await mutate();
    } catch (error) {
      handleAuthError(error);
      mutate(data); // Reverte em caso de erro
      throw error; 
    }
  }

  return { data, error, isLoading, addReserva, deleteReserva, putReserva};
};
export const useReservations = () => {

  const {token, logout} = useAuth()
  const {data, error, isLoading, addReserva, deleteReserva, putReserva} = _useReservations(token, logout)
  
  // Acesso mais seguro aos dados para evitar erros
  const reservations = !isLoading && data && data.details ? data.details.map(api2reserva) : []

  return { reservations, error, isLoading, addReserva, deleteReserva, putReserva};
}

export const useReservation = (reservaId) => {
  const { data, error, isLoading, mutate, addReserva, deleteReserva } = useSWR(reservaId ? `/reservations/${reservaId}` : null, fetcher);

  const reservation = !isLoading && data && data.details ? api2reserva(data.details) : data

  return { reservation, error, isLoading, mutate, deleteReserva };
}

export function useAuth() {
  const [token, setToken] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const storedToken = localStorage.getItem('jwt')
    if (storedToken) {
      setToken(storedToken)
    }
    setLoading(false) // Garante que o loading termine mesmo sem token
  }, [])

  const _login = async (email, password ) => {
    setLoading(true)
    setError(null)
    try {

      const req = await fetch(
        `${API_BASE_URL}/login`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email,
            password
          })
        }
      )

      if (req.status == 401) 
          throw new Error('Invalid credentials')

      const json = await req.json()
      const token = json.details.token
      localStorage.setItem('jwt', token)
      setToken(token)


    } catch (err) {
      setError(err.message)
      console.error('Login error: ', err.message)
    } finally {
      setLoading(false)
    }
  }

  const login = (email, password) => {
    useEffect(() => {
      _login(email, password)
    }, [])
  }

 const logout = () => {
    localStorage.removeItem('jwt')
    setToken(null)

  }

  return {token, login, logout, loading, error}
}

export function useUser(token) {

  
  const user = useSWR(token ? ['/user', token] : null, ([url,token]) => fetcher_jwt(url, token))

  return !user.data ? {isLoading: true} : user
}

