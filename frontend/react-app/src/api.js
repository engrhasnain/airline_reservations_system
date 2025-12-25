const API_BASE = import.meta.env.VITE_API_BASE || '/api'
import { getToken } from './utils/auth'

async function request(path, options={}){
  const token = getToken()
  const headers = options.headers || {}
  if (token) headers['Authorization'] = `Bearer ${token}`
  if (options.body && !headers['Content-Type']) headers['Content-Type'] = 'application/json'

  const res = await fetch(API_BASE + path, { ...options, headers })
  if (!res.ok){
    const text = await res.text()
    throw new Error(text || res.statusText)
  }
  return res.json().catch(()=>null)
}

export async function register(user){
  return request('/auth/register', {method: 'POST', body: JSON.stringify(user)})
}

export async function login(data){
  return request('/auth/login', {method: 'POST', body: JSON.stringify(data)})
}

export async function listFlights(){
  return request('/flights/')
}

export async function searchFlights(q){
  const params = new URLSearchParams(q)
  return request('/flights/search/for?' + params.toString())
}

export async function createBooking(flight_id){
  return request('/bookings/', {method: 'POST', body: JSON.stringify({flight_id})})
}

export async function pay(booking_id, amount){
  return request('/payments/', { method: 'POST', body: JSON.stringify({ booking_id, amount }) })
}

export default function api(path, options={}){ return request(path, options) }
