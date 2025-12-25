import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api, { listFlights, searchFlights, createBooking } from '../api'
import { getToken } from '../utils/auth'
import { fetchBookings } from '../services/bookings'
import CheckoutModal from '../components/CheckoutModal' 

export default function Flights(){
  const navigate = useNavigate()
  const [flights, setFlights] = useState([])
  const [origin, setOrigin] = useState('')
  const [destination, setDestination] = useState('')
  // Use datetime-local input so users can specify date + time
  const [date, setDate] = useState('')
  const [loadingIds, setLoadingIds] = useState(new Set())
  const [modalBookingId, setModalBookingId] = useState(null)
  const [seatMap, setSeatMap] = useState({})
  const [userBookingsMap, setUserBookingsMap] = useState({})

  async function loadUserBookings(){
    const token = getToken()
    if (!token){ setUserBookingsMap({}); return }
    try{
      const bs = await fetchBookings()
      const map = {}
      (bs || []).forEach(b => { map[b.flight_id] = b })
      setUserBookingsMap(map)
    }catch(err){
      setUserBookingsMap({})
    }
  }

  useEffect(()=>{ 
    listFlights()
      .then(res => { setFlights(res); fetchSeatsForFlights(res); loadUserBookings() })
      .catch(()=>setFlights([]))
  }, [])

  async function handleSearch(e){
    e.preventDefault()
    if (!origin || !destination || !date) return alert('Please provide origin, destination and date')
    try{
      const res = await searchFlights({origin, destination, date})
      setFlights(res)
      fetchSeatsForFlights(res)
      loadUserBookings()
    }catch(err){
      alert('Search failed: ' + err.message)
    }
  }

  async function handleBook(e, flight_id){
    e.stopPropagation()
    e.preventDefault()

    // ensure we have latest bookings for this user and prevent duplicate booking
    await loadUserBookings()
    if (userBookingsMap[flight_id]){
      return alert('You already have a booking for this flight (#' + userBookingsMap[flight_id].id + ')')
    }

    try{
      const token = getToken()
      if (!token) return alert('Please login to book')
      setLoadingIds(prev => new Set(prev).add(flight_id))
      const booking = await createBooking(flight_id)
      alert('Booking created: #' + booking.id)
      // open checkout modal to optionally pay
      setModalBookingId(booking.id)

      // refresh seats for this flight (seat may now be booked)
      try{
        const seats = await api(`/flights/${flight_id}/seats`)
        setSeatMap(prev => ({...prev, [flight_id]: seats}))
      }catch(e){
        // ignore
      }

      // refresh user bookings so UI reflects newly created booking
      try{ await loadUserBookings() }catch(e){}

    }catch(err){
      alert('Booking failed: ' + err.message)
    }finally{
      setLoadingIds(prev => {
        const copy = new Set(prev)
        copy.delete(flight_id)
        return copy
      })
    }
  }

  async function fetchSeatsForFlights(flights){
    if (!flights || flights.length === 0){
      setSeatMap({})
      return
    }
    try{
      const promises = flights.map(f => api(`/flights/${f.id}/seats`))
      const results = await Promise.all(promises)
      const map = {}
      flights.forEach((f, idx) => { map[f.id] = results[idx] || [] })
      setSeatMap(map)
    }catch(err){
      console.error('Failed to load seats', err)
    }
  }

  return (
    <div className="max-w-5xl mx-auto py-10">
      <h2 className="text-2xl font-semibold mb-4">Search Flights</h2>
      <form className="mb-4 flex gap-2" onSubmit={handleSearch}>
        <input className="p-2 border rounded flex-1" placeholder="origin" value={origin} onChange={e=>setOrigin(e.target.value)} />
        <input className="p-2 border rounded flex-1" placeholder="destination" value={destination} onChange={e=>setDestination(e.target.value)} />
        <input className="p-2 border rounded" type="date" value={date} onChange={e=>setDate(e.target.value)} />
        <button className="bg-emerald-500 text-white px-4 rounded">Search</button>
      </form>

      <div className="grid md:grid-cols-2 gap-4">
        {flights?.map(f=> {
          const seats = seatMap[f.id] || []
          const availableSeats = seats.filter(s => !s.is_booked)
          return (
          <div key={f.id} className="card hover:shadow-lg transition">
            <div className="flex items-center gap-4">
              <div className="flex-1">
                <Link to={`/flights/${f.id}`} className="block hover:underline">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-lg font-semibold">{f.flight_number}</div>
                      <div className="text-sm text-slate-600">{f.origin} → {f.destination}</div>
                    </div>
                    <div className="text-sm text-slate-500">{new Date(f.departure_time).toLocaleString()}</div>
                  </div>
                  <div className="mt-2 text-sm text-slate-500">Departs: {new Date(f.departure_time).toLocaleString()} • Arrives: {new Date(f.arrival_time).toLocaleString()}</div>
                </Link>
                <div className="mt-2">
                  <div className="text-sm text-slate-600">Available seats: {availableSeats.length}</div>
                  <div className="mt-1 flex gap-1 flex-wrap">
                    {availableSeats.slice(0,6).map(s => (
                      <span key={s.id} className="px-2 py-0.5 text-xs border rounded bg-slate-50">{s.seat_number}</span>
                    ))}
                    {availableSeats.length > 6 && <span className="px-2 py-0.5 text-xs text-slate-500">+{availableSeats.length - 6}</span>}
                  </div>
                </div>
              </div>
              {userBookingsMap[f.id] ? (
                <div className="text-right">
                  <div className="text-sm text-emerald-600">Booked #{userBookingsMap[f.id].id}</div>
                  <a href="/dashboard" className="text-xs text-slate-500">View booking</a>
                </div>
              ) : (
                <div className="flex flex-col items-end gap-2">
                  <div className="text-xs text-slate-500">Seats</div>
                  <button onClick={(e)=>handleBook(e, f.id)} disabled={loadingIds.has(f.id)} className="bg-emerald-500 text-white px-3 py-1 rounded disabled:opacity-50">{loadingIds.has(f.id) ? 'Booking...' : 'Book'}</button>
                </div>
              )}
            </div>
          </div>
        )})}
      </div>
      <CheckoutModal isOpen={!!modalBookingId} bookingId={modalBookingId} onClose={() => { setModalBookingId(null); navigate('/dashboard') }} onPaid={() => { navigate('/dashboard') }} />
    </div>
  )
}
