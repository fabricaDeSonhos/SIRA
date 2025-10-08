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
  
  // optimal: function: cache -> new-cache
  const backend_call = async (url, method, optimal, body) => {

    // Optimistic update: Immediately update the local cache
    const optimisticData = data


    // Update local cache based on otpimal
    optimisticData.details = optimal(optimisticData.details)
    mutate(optimisticData, false);

    try {
      // Make the POST request to the API
      const req = await fetch(`${API_BASE_URL}/${url}`, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(body),
      });
      const json = await req.json()

      if (!req.ok)
        throw json
      // Re-validate the data from the server
      mutate();

      return json
    } catch (e) {
      // Revert to the previous data if the request fails
      mutate(data);
      console.error("Failed to add item:", e);
      return e
    }
  } 

  const addReserva = async (newItem) => backend_call("reservations", "POST", (data) => [...(data || []), newItem], newItem)
  const deleteReserva = async (reservaId) => backend_call(`reservations/${reservaId}`, "DELETE", data => data.filter(u => u.id !== reservaId), {})
  const putReserva = async (reservaId, changesObj) => backend_call(`reservations/${reservaId}`, "PUT", 
	  data => {
	    const i = data.findIndex(x => x.id == reservaId)
	    update_obj(data[i], changesObj)
	    return data

	  },
	  changesObj 
  )

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

