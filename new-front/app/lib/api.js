
import useSWR from 'swr';
import {useState, useEffect} from 'react'
import {tempo_para_número} from './tempo.js'

const API_BASE_URL = "http://localhost:5000";

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

function api2reserva(api_res) {
  const hoje = new Date()
  const diaHoje = hoje.toISOString().slice(0, 10)

  const id = api_res.id
  const lab = api_res.room_id
  const matéria = api_res.purpose
  const dia = diaHoje
  const início = tempo_para_número(api_res.start_time)
  const duração = tempo_para_número(api_res.end_time) - início

  return {id, lab, matéria, dia, início, duração: duração*60}
}


const _useReservations = (token) => {
  const { data, error, isLoading, mutate } = useSWR('/reservations', fetcher);
  
  const addReserva = async (newItem) => {

    // Optimistic update: Immediately update the local cache
    const optimisticData = data
    optimisticData.details = [...(optimisticData.details || []), newItem]
    mutate(optimisticData, false);

    try {
      // Make the POST request to the API
      await fetch(`${API_BASE_URL}/reservations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(newItem),
      });

      // Re-validate the data from the server
      mutate();
    } catch (e) {
      // Revert to the previous data if the request fails
      mutate(data);
      console.error("Failed to add item:", e);
    }
  };

  const deleteReserva = async (reservaId) => {
      // Optimistic update
      const optimisticData = data
      optimisticData.details = data.details.filter((u) => u.id !== reservaId);

      mutate(optimisticData, false);

      try {
        await fetch(`${API_BASE_URL}/reservations/${reservaId}`, {
          method: 'DELETE',
          headers: {
          "Authorization": 'Bearer ' + token, 
        }

        });
        // Re-fetch
        mutate();
      } catch (error) {
        // Revert
        mutate(data);
      }
    };

  // changesObj is a reservation object, only edited values are present
  const putReserva = async (reservaId, changesObj) => {
    const od = data 

    const i = od.details.findIndex(x => x.id == reservaId)
    update_obj(od.details[i], changesObj)

    mutate(od, false)

    try {
      await fetch(`${API_BASE_URL}/reservations/${reservaId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token 
        },
        body: JSON.stringify(changesObj)
      })
      mutate()
    } catch (error) {
      mutate(data)
    }
  }

  return { data, error, isLoading, addReserva, deleteReserva, putReserva};
};
export const useReservations = () => {

  const {token} = useAuth()
  const {data, error, isLoading, mutate, addReserva, deleteReserva, putReserva} = _useReservations(token)
  console.log(data)
  const reservations = !isLoading ? data.details.map(api2reserva) : data

  return { reservations, error, isLoading, addReserva, deleteReserva, putReserva};
}

export const useReservation = (reservaId) => {
  const { data, error, isLoading, mutate, addReserva, deleteReserva } = useSWR(reservaId ? `/reservations/${reservaId}` : null, fetcher);

  const reservation = !isLoading ? api2reserva(data.details) : data

  return { reservation, error, isLoading, mutate, deleteReserva };
}

export function useAuth() {
  const [token, setToken] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const storedToken = localStorage.getItem('jwt')
    if (storedToken)
      setToken(storedToken)

    setLoading(false)
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
